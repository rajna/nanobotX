---
name: skill-chain-optimizer-before-context
description: 基于用户反馈的任务评分和新任务记录
trigger:
  event: before_context_build
  priority: 100
---

# Before Context Build Hook

在构建上下文之前触发：
1. 分析用户反馈，判断上一个任务的成功/失败
2. 根据用户反馈调整评分
3. 保存并优化上一个任务
4. 记录新任务开始时间
