---
name: chinese-classical
description: 将中文转换为文言文以节省 token
version: 3.0.0
---

# Chinese Classical Skill

将历史消息中的现代中文转换为文言文，节省上下文 token 使用量。

## 功能

- **LLM 压缩**：智能，40-60% 压缩率
- **Token 阈值过滤**：只压缩 > min_tokens 的消息
- **技术内容检测**：跳过代码/技术内容占比过高的消息
- **概率触发**：避免频繁使用 LLM
- 自动跳过已压缩消息
- 保护代码、URL、数字不被转换
- 最近 N 条消息保持原样

## 配置

```json
{
  "hooks": {
    "hook_options": {
      "chinese-classical": {
        "skip_recent": 3,
        "min_tokens": 500,
        "tech_ratio": 0.3,
        "probability": 0.5,
        "enable_llm": true,
        "llm_min_length": 50,
        "llm_max_length": 4000
      }
    }
  }
}
```

## 配置说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `skip_recent` | 3 | 最近 N 条消息保持原样 |
| `min_tokens` | 500 | 只压缩大于此 token 数的消息 |
| `tech_ratio` | 0.3 | 技术内容最大占比（超过则跳过） |
| `probability` | 0.5 | 压缩触发概率（避免频繁使用） |
| `enable_llm` | true | 是否启用 LLM 压缩 |
| `llm_min_length` | 50 | 最小压缩长度（小于此值不压缩） |
| `llm_max_length` | 4000 | 最大压缩长度（超过此值分段压缩） |

## 版本更新

**v3.0.0** (2026-03-13):
- 新增 `min_tokens` 配置：只压缩大于此 token 数的消息（默认 500）
- 新增 `tech_ratio` 配置：跳过技术内容占比过高的消息（默认 30%）
- 新增 `probability` 配置：概率触发压缩，避免频繁使用（默认 50%）
- 优化技术内容检测：代码块、URL、英文单词等
- 详细的跳过原因日志

**v2.0.0** (2026-03-12):
- 移除规则压缩，只使用 LLM 压缩
- 提高压缩质量和一致性
- 更好的 token 节省效果

## 日志示例

```
Hook 'chinese-classical': 10 msgs (2 compressed), LLM: True, min_tokens: 500, tech_ratio: 30%, probability: 50%
Hook 'chinese-classical': compressed 1, saved 120 chars (15.0%), skips: below_token_threshold(350<500)=3, too_much_tech_content(45%>30%)=2, probability_skip(0.78>0.50)=2
```

## 跳过原因说明

| 原因 | 说明 |
|------|------|
| `recent` | 最近 N 条消息 |
| `special` | 工具调用或系统消息 |
| `no_content` | 无内容 |
| `too_short` | 长度小于 min_length |
| `below_token_threshold` | Token 数小于 min_tokens |
| `too_much_tech_content` | 技术内容占比超过 tech_ratio |
| `probability_skip` | 随机跳过（概率控制） |
| `no_compression` | 压缩效果不明显 |