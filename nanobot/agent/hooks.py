
# -*- coding: utf-8 -*-
"""
Hook System for nanobot - 统一版

所有 Hooks 都在 Skills 中：
nanobot/skills/
├── chinese-classical/           # Hook 作为 Skill
│   ├── SKILL.md
│   └── hooks/
│       └── main/
│           ├── hook.md
│           └── hook.py
└── self-improving-agent/        # 带 Hook 的 Skill
    ├── SKILL.md
    └── hooks/
        ├── on-error/
        └── on-correction/
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from loguru import logger


class HookEvent(str, Enum):
    """支持的 Hook 事件"""
    # 上下文相关
    BEFORE_CONTEXT_BUILD = "before_context_build"
    AFTER_CONTEXT_BUILD = "after_context_build"
    
    # LLM 相关
    BEFORE_LLM_CALL = "before_llm_call"
    AFTER_LLM_CALL = "after_llm_call"
    
    # 工具相关
    BEFORE_TOOL_CALL = "before_tool_call"
    AFTER_TOOL_CALL = "after_tool_call"
    
    # 消息相关
    ON_MESSAGE = "on_message"
    ON_RESPONSE = "on_response"
    
    # 错误和学习
    ON_ERROR = "on_error"
    ON_CORRECTION = "on_correction"
    ON_LEARNING = "on_learning"
    
    # 会话相关
    ON_SESSION_START = "on_session_start"
    ON_SESSION_END = "on_session_end"
    ON_BOOTSTRAP = "on_bootstrap"
    
    # 用户反馈
    ON_FEEDBACK = "on_feedback"


@dataclass
class HookInfo:
    """Hook 信息"""
    name: str
    event: str
    priority: int = 100
    path: Path | None = None
    description: str = ""
    skill_name: str = ""  # 所属 Skill
    sync_func: Callable | None = None
    async_func: Callable | None = None
    loaded: bool = False
    enabled: bool = True


@dataclass
class HookConfig:
    """Hook 配置"""
    enabled: bool = True
    disabled_hooks: list[str] = field(default_factory=list)
    hook_options: dict[str, dict[str, Any]] = field(default_factory=dict)


class HookManager:
    """
    Hook 管理器 - 统一版
    
    所有 Hooks 都从 Skills 目录发现：
    nanobot/skills/{skill-name}/hooks/{hook-name}/
    """

    def __init__(
        self,
        skills_dir: Path,
        config: HookConfig | None = None,
    ):
        self.skills_dir = skills_dir
        self.config = config or HookConfig()

        self._hooks: dict[str, list[HookInfo]] = {}
        self._all_hooks: dict[str, HookInfo] = {}

        self._discover_hooks()

    def _parse_hook_md(self, content: str) -> dict[str, Any]:
        """解析 hook.md frontmatter"""
        if not content.startswith("---"):
            return {}

        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return {}

        frontmatter = {}
        current_key = None
        current_value = []

        for line in match.group(1).split("\n"):
            if line.startswith("  ") and current_key:
                current_value.append(line.strip())
            elif ":" in line:
                if current_key and current_value:
                    frontmatter[current_key] = (
                        "\n".join(current_value)
                        if len(current_value) > 1
                        else current_value[0]
                    )
                    current_value = []
                key, value = line.split(":", 1)
                current_key = key.strip()
                current_value = [value.strip()] if value.strip() else []

        if current_key and current_value:
            frontmatter[current_key] = (
                "\n".join(current_value)
                if len(current_value) > 1
                else current_value[0]
            )

        return frontmatter

    def _parse_trigger(self, trigger_str: str) -> tuple[str, int]:
        """解析 trigger 配置"""
        event = "before_llm_call"
        priority = 100

        for line in str(trigger_str).split("\n"):
            line = line.strip()
            if line.startswith("event:"):
                event = line.split(":", 1)[1].strip()
            elif line.startswith("priority:"):
                try:
                    priority = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

        return event, priority

    def _discover_hooks(self) -> None:
        """从 Skills 目录发现所有 Hooks"""
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return

        logger.debug(f"Scanning skills for hooks: {self.skills_dir}")

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            hooks_dir = skill_dir / "hooks"
            
            if not hooks_dir.exists():
                continue

            # 发现该 Skill 下的所有 Hooks
            for hook_dir in hooks_dir.iterdir():
                if not hook_dir.is_dir():
                    continue

                hook_md = hook_dir / "hook.md"
                if not hook_md.exists():
                    continue

                try:
                    content = hook_md.read_text(encoding="utf-8")
                    frontmatter = self._parse_hook_md(content)

                    name = frontmatter.get("name", f"{skill_name}-{hook_dir.name}")

                    if name in self._all_hooks:
                        continue

                    if name in self.config.disabled_hooks:
                        logger.info(f"Hook disabled: {name}")
                        continue

                    trigger = frontmatter.get("trigger", "")
                    event, priority = self._parse_trigger(str(trigger))

                    hook_info = HookInfo(
                        name=name,
                        event=event,
                        priority=priority,
                        path=hook_dir,
                        description=frontmatter.get("description", ""),
                        skill_name=skill_name,
                    )

                    if event not in self._hooks:
                        self._hooks[event] = []
                    self._hooks[event].append(hook_info)
                    self._all_hooks[name] = hook_info

                    logger.info(f"✓ Hook: {name} (skill={skill_name}, event={event})")

                except Exception as e:
                    logger.error(f"Failed to parse hook {hook_dir}: {e}")

        # 按优先级排序
        for event in self._hooks:
            self._hooks[event].sort(key=lambda h: h.priority)

        # 统计
        total = sum(len(hooks) for hooks in self._hooks.values())
        if total > 0:
            logger.info(f"Total hooks discovered: {total}")

    def _load_hook(self, hook: HookInfo) -> bool:
        """加载 Hook 脚本"""
        if hook.loaded:
            return True

        if not hook.path:
            return False

        # 查找 Hook 脚本
        hook_script = None
        for name in ["hook", "handler", "main", "index"]:
            script_path = hook.path / f"{name}.py"
            if script_path.exists():
                hook_script = script_path
                break

        if not hook_script:
            logger.warning(f"No hook script found for: {hook.name}")
            return False

        try:
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location(
                f"hook_{hook.name}",
                hook_script,
            )
            if spec is None or spec.loader is None:
                return False

            module = importlib.util.module_from_spec(spec)
            sys.modules[f"hook_{hook.name}"] = module
            spec.loader.exec_module(module)

            if hasattr(module, "execute"):
                func = module.execute
                if asyncio.iscoroutinefunction(func):
                    hook.async_func = func
                else:
                    hook.sync_func = func

            hook.loaded = True
            return True

        except Exception as e:
            logger.error(f"Failed to load hook {hook.name}: {e}")
            return False

    def list_hooks(self, event: str | None = None) -> list[dict[str, Any]]:
        """列出 Hooks"""
        if event:
            hooks = self._hooks.get(event, [])
            return [
                {
                    "name": h.name,
                    "event": h.event,
                    "priority": h.priority,
                    "skill": h.skill_name,
                }
                for h in hooks
            ]

        return [
            {
                "name": h.name,
                "event": h.event,
                "priority": h.priority,
                "skill": h.skill_name,
            }
            for h in self._all_hooks.values()
        ]

    def is_enabled(self) -> bool:
        return self.config.enabled

    async def trigger_async(
        self,
        event: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """触发 Hook（异步）"""
        if not self.config.enabled:
            return context

        hooks = self._hooks.get(event, [])
        if not hooks:
            return context

        result = context
        for hook in hooks:
            if not hook.enabled:
                continue

            if not self._load_hook(hook):
                continue

            try:
                hook_options = self.config.hook_options.get(hook.name, {})
                hook_context = {**result, "_options": hook_options}

                if hook.async_func is not None:
                    result = await hook.async_func(hook_context)
                elif hook.sync_func is not None:
                    result = hook.sync_func(hook_context)

                logger.debug(f"Hook '{hook.name}' executed for event '{event}'")

            except Exception as e:
                logger.error(f"Hook '{hook.name}' failed: {e}")

        return result


def create_hook_manager(
    skills_dir: Path,
    config: dict[str, Any] | None = None,
) -> HookManager:
    """创建 Hook 管理器"""
    hook_config = HookConfig()

    if config:
        if isinstance(config, dict):
            hook_config.enabled = config.get("enabled", True)
            hook_config.disabled_hooks = config.get("disabled_hooks", [])
            hook_config.hook_options = config.get("hook_options", {})

    return HookManager(skills_dir=skills_dir, config=hook_config)