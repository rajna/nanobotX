---
name: skill-chain-optimizer-record
description: 记录工具调用
trigger:
  event: after_tool_call
  priority: 100
---

# After Tool Call Hook

在工具调用后记录：
1. 工具名称
2. 执行时长
3. 成功状态
