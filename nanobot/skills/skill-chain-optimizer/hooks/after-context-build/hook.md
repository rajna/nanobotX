---
name: skill-chain-optimizer-recommend
description: 推荐最佳 skill chain
trigger:
  event: after_context_build
  priority: 100
---

# After Context Build Hook

在构建上下文之后触发：
1. 获取用户消息
2. 查找相似任务
3. 推荐最佳 skill chain
