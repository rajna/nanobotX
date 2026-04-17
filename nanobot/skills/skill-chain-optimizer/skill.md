---
name: skill-chain-optimizer
description: "智能推荐、记录和优化Agent任务的技能调用链。支持自动评分、相似任务匹配、历史链管理。"
version: 7.7.0
hooks:
  - event: before_context_build
    path: hooks/before-context-build
    priority: 100
  - event: after_context_build
    path: hooks/after-context-build
    priority: 100
  - event: after_tool_call
    path: hooks/after-tool-call
    priority: 100
---

# Skill Chain Optimizer: 技能调用链优化器

智能推荐、记录和优化Agent任务的技能调用链。

## Hook 支持

| Hook | 事件 | 功能 |
|------|------|------|
| before_context_build | 构建上下文前 | 分析用户反馈 → 判断上一个任务成功/失败 → 保存并打分 |
| after_context_build | 构建上下文后 | 推荐最佳 skill chain |
| after_tool_call | 工具调用后 | 记录 skill 调用 |

## 工作流程

```
用户发消息 → 分析反馈（AI评价） → 保存并打分上一个任务 → 记录新任务开始 → 推荐最佳链 → 执行工具 → 记录调用
```

## 任务抽象化

为了提高技能链的复用性，系统会自动将具体的任务描述抽象化为通用类别：

| 用户消息 | 抽象任务 |
|----------|----------|
| "分析拓维信息" | "分析股票" |
| "分析朝阳科技" | "分析股票" |
| "查询天气" | "查询天气" |
| "搜索xxx" | "搜索信息" |

这样下次分析任何股票时，都能推荐到之前成功的技能链。

## 用户反馈评分

### AI评价（优先）

系统会使用AI来分析用户反馈，判断任务完成情况并给出评分系数：

| 评分系数 | 含义 | 示例反馈 |
|----------|------|----------|
| 1.5 | 非常满意 | "太棒了！"、"完美！"、"超出预期" |
| 1.2 | 满意 | "很好"、"不错"、"解决了" |
| 1.0 | 一般 | "可以"、"还行"、"基本完成" |
| 0.8 | 不太满意 | "有点问题"、"不太对"、"需要改进" |
| 0.5 | 不满意 | "不对"、"错误"、"失败" |

### 规则匹配（回退）

如果AI评价失败，系统会回退到规则匹配：

| 用户反馈 | 任务状态 | 评分系数 |
|----------|----------|----------|
| "很好"、"谢谢"、"解决了" | ✅ 成功 | ×1.2 |
| "不对"、"错误"、"重试" | ❌ 失败 | ×0.5 |
| 其他 | ✅ 完成 | ×1.0 |

## 配置

```json
{
  "hooks": {
    "hook_options": {
      "skill-chain-optimizer": {
        "storage_path": "~/.nanobot/data/skill-chains",
        "similarity_threshold": 0.35,
        "max_chains_per_task": 5
      }
    }
  }
}
```

## 日志示例

```
Hook 'skill-chain-optimizer': 新任务开始: 分析股票 (原始: 分析拓维信息)
Hook 'skill-chain-optimizer': AI评价反馈 - 完成: true, 系数: 1.20
Hook 'skill-chain-optimizer': 推荐链 [stock-data-fetcher] (置信度: 92%, 评分: 88)
Hook 'skill-chain-optimizer': 从 exec 命令中提取 skill 名称: horoscope-fetcher
Hook 'skill-chain-optimizer': 记录调用 horoscope-fetcher (1200ms)
Hook 'skill-chain-optimizer': 任务完成 [stock-data-fetcher] 耗时: 3.5s 基础分: 75 反馈系数: 1.2 最终分: 90/100
```

## 更新日志

### v7.7.0 (2026-03-13)
- **修复**: `after_tool_call` hook 现在能正确识别通过 `exec` 调用的 skill
  - 从 `exec` 命令中提取 skill 名称（如 `horoscope-fetcher`）
  - 不再记录为 `exec`，而是记录实际的 skill 名称
  - 示例：`python3 .../skills/horoscope-fetcher/scripts/...` → 记录为 `horoscope-fetcher`

### v7.6.0 (2026-03-13)
- 实现 AI 评价系统，使用 LLM 分析用户反馈并给出评分系数
- 修改 `agent/loop.py` 添加 provider 和 model 到 hook_context（待用户批准）

### v7.5.0 (2026-03-13)
- 添加任务抽象功能，将具体任务抽象化为通用类别
- 提高技能链的复用性

### v7.4.0 (2026-03-13)
- 修复 hook context 传递问题，使用 `hook_context.update()` 防止上下文丢失