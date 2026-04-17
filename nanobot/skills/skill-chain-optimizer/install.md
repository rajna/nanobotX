# 创建安装说明
cat > /home/z/my-project/nanobot-hook-files/skill-chain-optimizer-hook/INSTALL.md << 'EOF'
# Skill Chain Optimizer - Hook 版本安装说明

## 文件结构

```
nanobot/
├── agent/
│   └── hooks.py                    # Hook 管理器
└── skills/
    └── skill-chain-optimizer/
        ├── SKILL.md
        ├── scripts/
        │   └── skill_chain_optimizer.py
        └── hooks/
            ├── on-session-start/
            │   ├── HOOK.md
            │   └── hook.py
            ├── after-tool-call/
            │   ├── HOOK.md
            │   └── hook.py
            └── on-session-end/
                ├── HOOK.md
                └── hook.py
```

## 安装步骤

### 1. 复制文件

```bash
# 复制 hooks.py
cp agent/hooks.py /path/to/nanobot/nanobot/agent/

# 复制 skill
cp -r skills/skill-chain-optimizer /path/to/nanobot/nanobot/skills/
```

### 2. 修改 loop.py

参考 LOOP_PATCH.md 添加 Hook 触发点：

- `ON_SESSION_START`: 会话开始时
- `AFTER_TOOL_CALL`: 工具调用后
- `ON_SESSION_END`: 会话结束时

### 3. 配置

```json
{
  "hooks": {
    "enabled": true,
    "hook_options": {
      "skill-chain-optimizer-start": {
        "storage_path": "~/.nanobot/data/skill-chains",
        "similarity_threshold": 0.35,
        "max_chains_per_task": 5
      }
    }
  }
}
```

### 4. 验证

启动后应该看到：

```
✓ Hook: skill-chain-optimizer-start (skill=skill-chain-optimizer, event=on_session_start)
✓ Hook: skill-chain-optimizer-record (skill=skill-chain-optimizer, event=after_tool_call)
✓ Hook: skill-chain-optimizer-end (skill=skill-chain-optimizer, event=on_session_end)
Total hooks discovered: 3
```

## 工作流程

```
用户发送消息
    │
    ▼
┌─────────────────────────────────┐
│ ON_SESSION_START                │
│ → 推荐最佳 skill chain          │
│ → 注入 _optimizer 到 context    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ 工具调用 (如 stock-query)        │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ AFTER_TOOL_CALL                 │
│ → 记录 skill 调用                │
│ → 保存到 current_skill_calls    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ 更多工具调用...                  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ ON_SESSION_END                  │
│ → 保存 skill chain              │
│ → 自动评分                       │
│ → 更新最佳链                     │
└─────────────────────────────────┘
```

## 日志示例

```
Hook 'skill-chain-optimizer': 推荐链 [stock-query, web-search, LLM] (置信度: 85%, 评分: 92)
Hook 'skill-chain-optimizer': 记录调用 stock-query ✓ (1500ms)
Hook 'skill-chain-optimizer': 记录调用 web-search ✓ (2000ms)
Hook 'skill-chain-optimizer': 记录调用 LLM ✓ (3000ms)
Hook 'skill-chain-optimizer': 保存链 [stock-query, web-search, LLM] 评分: 92/100
Hook 'skill-chain-optimizer': 🏆 这是目前最佳方案！
```
EOF

echo "✓ 已创建 INSTALL.md"
echo ""
echo "=== 最终文件列表 ==="
find /home/z/my-project/nanobot-hook-files/skill-chain-optimizer-hook -type f | sort