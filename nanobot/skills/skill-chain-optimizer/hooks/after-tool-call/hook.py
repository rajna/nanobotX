"""
After Tool Call Hook - 记录 skill 调用

在工具调用后记录：
1. 工具名称
2. 执行时长
3. 成功状态
"""
from __future__ import annotations

from typing import Any
import time


async def execute(context: dict[str, Any]) -> dict[str, Any]:
    """Hook 入口函数"""
    from loguru import logger
    import re
    
    tool_result = context.get("tool_result", {})

    # 优先从 tool_calls 中提取 skill 名称
    tool_name = "unknown"
    tool_args = context.get("tool_args", {})
    tool_calls = context.get("tool_calls", [])
    logger.info(f"Hook 'skill-chain-optimizer': tool_calls = {tool_calls}")

    # 1. 尝试从 tool_calls 中提取 skill 名称
    if tool_calls:
        for tool_call in tool_calls:
            if isinstance(tool_call, dict):
                # 修正：arguments 在 function 下
                function = tool_call.get("function", {})
                logger.info(f"Hook 'skill-chain-optimizer': function = {function}")
                arguments = function.get("arguments", "")
                logger.info(f"Hook 'skill-chain-optimizer': arguments = {arguments}")
                # 处理 arguments 可能是 JSON 字符串的情况
                if isinstance(arguments, str):
                    import json
                    try:
                        arguments = json.loads(arguments)
                        logger.info(f"Hook 'skill-chain-optimizer': parsed arguments = {arguments}")
                    except json.JSONDecodeError as e:
                        logger.info(f"Hook 'skill-chain-optimizer': JSON parse error: {e}")
                        arguments = {}
                # 从 command 字段中提取 skill 名称
                command = arguments.get("command", "")
                logger.info(f"Hook 'skill-chain-optimizer': command = {command}")
                if command:
                    match = re.search(r'/skills/([\w-]+)', command)
                    if match:
                        tool_name = match.group(1)
                        logger.info(f"Hook 'skill-chain-optimizer': 从 tool_calls 中提取 skill 名称: {tool_name}")
                        break

    # 2. 如果 tool_calls 中没有匹配到，尝试从 exec 命令中提取 skill 名称
    if tool_name == "unknown" and tool_args.get("command"):
        command = tool_args.get("command", "")
        #logger.info(f"Hook 'skill-chain-optimizer': tool_args command = {command}")
        # 匹配模式: skills/{skill-name}/scripts/
        match = re.search(r'/skills/([^/]+)/scripts/', command)
        if match:
            tool_name = match.group(1)
            logger.info(f"Hook 'skill-chain-optimizer': 从 exec 命令中提取 skill 名称: {tool_name}")

    # 3. 如果命令中没有匹配到，尝试从上下文消息中提取 skill 名称
    if tool_name == "unknown":
        messages = context.get("messages", [])
        # logger.info(f"Hook 'skill-chain-optimizer': messages = {messages[-1]}")
        # 从最近的几条消息中查找 skill 名称
        for msg in reversed(messages[-5:]):  # 检查最近5条消息
            if isinstance(msg, dict):
                # 从 tool_calls 中提取 skill 名称
                tool_calls = msg.get("tool_calls", [])
                # logger.info(f"Hook 'skill-chain-optimizer': msg tool_calls = {tool_calls}")
                if tool_calls:
                    for tool_call in tool_calls:
                        if isinstance(tool_call, dict):
                            function = tool_call.get("function", {})
                            arguments = function.get("arguments", "")
                            # 处理 arguments 可能是 JSON 字符串的情况
                            if isinstance(arguments, str):
                                import json
                                try:
                                    arguments = json.loads(arguments)
                                except json.JSONDecodeError:
                                    arguments = {}
                            command = arguments.get("command", "")
                            # logger.info(f"Hook 'skill-chain-optimizer': msg command = {command}")
                            if command:
                                pattern = r'/skills/([\w-]+)' 
                                match = re.search(pattern, command)
                                if match:
                                    tool_name = match.group(1)
                                    logger.info(f"Hook 'skill-chain-optimizer': 从上下文消息中提取 skill 名称: {tool_name}")
                                    break
                    if tool_name != "unknown":
                        break

    # 获取优化器实例
    optimizer = context.get("_optimizer")
    if not optimizer:
        return context

    # 判断成功状态
    success = True
    error_message = None

    if isinstance(tool_result, dict):
        if tool_result.get("error"):
            success = False
            error_message = str(tool_result.get("error"))
        elif tool_result.get("success") is False:
            success = False
            error_message = tool_result.get("message", "Unknown error")
    elif isinstance(tool_result, str):
        if "error" in tool_result.lower() or "failed" in tool_result.lower():
            success = False
            error_message = tool_result[:200]

    # 估算执行时长（如果没有精确数据）
    duration = context.get("duration", 1000)

    # 过滤掉 unknown 的记录
    if tool_name == "unknown":
        #logger.debug("Hook 'skill-chain-optimizer': 跳过 unknown 技能记录")
        return context

    try:
        optimizer.record_skill_call(
            skill_name=tool_name,
            duration=duration,
            success=success,
            input_data=context.get("tool_args", {}),
            output_data={"result": str(tool_result)[:500]} if tool_result else {},
            error_message=error_message,
        )

        status = "✓" if success else "✗"
        logger.debug(
            "Hook 'skill-chain-optimizer': 记录调用 {} {} ({}ms)",
            tool_name, status, duration
        )

    except Exception as e:
        logger.error(f"Hook 'skill-chain-optimizer' record failed: {e}")

    return context