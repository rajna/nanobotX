---
name: paper-to-skill
description: "A meta-skill that automatically generates new skills by analyzing high-quality academic papers. This skill searches for trending papers, extracts their core methodologies and thinking patterns, and transforms them into reusable AI skills. Use when you need to create new skills based on academic research, or when exploring how to convert scholarly insights into practical AI capabilities."
license: MIT
---

# Paper-to-Skill: 论文驱动的Skill生成器

这是一个元技能（Meta-Skill），用于从高质量学术论文中自动提取核心方法论，并将其转化为可复用的AI技能。

## 核心能力

### 1. 论文发现与筛选
- 自动搜索arXiv、Google Scholar等学术平台的热门论文
- 基于引用数、下载量、社交媒体热度筛选高质量论文
- 支持按领域（AI、NLP、CV、ML等）和时间段筛选

### 2. 论文深度分析
- 提取论文的核心方法论和思维框架
- 识别论文的创新点和关键贡献
- 分析论文的逻辑结构和推理模式
- 评估论文的实用性和可转化性

### 3. Skill自动生成
- 将论文方法论转化为结构化的skill定义
- 生成包含完整使用说明的SKILL.md文件
- 自动检测skill命名冲突（本地和ckawhub）
- 提供skill的使用案例和示例代码

## 工作流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  论文搜索阶段    │ ──▶ │  论文分析阶段    │ ──▶ │  Skill生成阶段   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  - arXiv搜索            - 方法论提取            - SKILL.md生成
  - 热度筛选             - 逻辑结构分析          - 命名冲突检测
  - 领域过滤             - 创新点识别            - 使用案例编写
```

## 使用方法

### 方式一：自动发现热门论文并生成Skill

```bash
# 搜索AI领域最近一周的热门论文，自动选择最佳论文生成skill
z-ai function -n paper_to_skill -a '{"action": "auto_discover", "field": "AI", "days": 7}'
```

### 方式二：指定论文URL生成Skill

```bash
# 从指定arXiv论文生成skill
z-ai function -n paper_to_skill -a '{
  "action": "generate_from_url",
  "paper_url": "https://arxiv.org/abs/2301.07041",
  "skill_name": "chain-of-thought"
}'
```

### 方式三：分析论文但不生成Skill（预览模式）

```bash
# 仅分析论文，输出分析报告
z-ai function -n paper_to_skill -a '{
  "action": "analyze_only",
  "paper_url": "https://arxiv.org/abs/2301.07041"
}'
```

## 详细操作指南

### 第一阶段：论文搜索

**目标**：发现高质量、高影响力的学术论文

**执行步骤**：

1. **确定搜索领域**
   - 支持的领域：AI/ML、NLP、Computer Vision、Robotics、Data Science等
   - 可指定子领域如：LLM、Transformer、Diffusion Models等

2. **构建搜索查询**
   ```javascript
   // 使用web-search skill搜索论文
   const searchQueries = [
     `site:arxiv.org ${field} trending papers ${year}`,
     `${field} breakthrough research high citations`,
     `best ${field} papers ${conference} ${year}`
   ];
   ```

3. **筛选高质量论文**
   - 检查论文引用数（Google Scholar）
   - 查看arXiv下载量和评分
   - 分析社交媒体讨论热度（Twitter/X, Reddit）
   - 优先选择：顶会论文、高引用论文、工业界关注论文

4. **输出候选论文列表**
   ```json
   {
     "candidates": [
       {
         "title": "Paper Title",
         "url": "https://arxiv.org/abs/xxxx.xxxxx",
         "citations": 1500,
         "field": "NLP",
         "relevance_score": 0.95
       }
     ]
   }
   ```

### 第二阶段：论文分析

**目标**：深度理解论文，提取可转化的方法论

**分析框架**：

1. **方法论提取（Methodology Extraction）**
   - 核心算法/模型是什么？
   - 关键步骤和流程是什么？
   - 需要什么输入，产生什么输出？

2. **思维模式分析（Thinking Pattern Analysis）**
   - 论文解决问题的思路是什么？
   - 有哪些创新性的思维框架？
   - 如何将这种思维方式泛化？

3. **实用性评估（Practicality Assessment）**
   - 方法是否容易实现？
   - 是否需要特殊资源（GPU、数据集）？
   - 对用户有什么实际价值？

4. **Skill适配性判断（Skill Adaptability）**
   - 是否适合转化为skill？
   - 转化后的skill能解决什么问题？
   - 预期的用户使用场景是什么？

**分析输出模板**：

```markdown
## 论文分析报告

### 基本信息
- 标题：[论文标题]
- 作者：[作者列表]
- 发表时间：[日期]
- 来源：[arXiv/会议/期刊]

### 核心方法论
[详细描述论文的核心方法]

### 思维框架
[描述论文解决问题的思维方式]

### 创新点
1. [创新点1]
2. [创新点2]
3. [创新点3]

### Skill转化建议
- 建议skill名称：[name]
- 核心功能：[功能描述]
- 适用场景：[场景列表]
```

### 第三阶段：Skill生成

**目标**：创建完整、可用的skill

**生成流程**：

1. **命名冲突检测**
   ```javascript
   // 检查本地skills目录
   const localSkills = fs.readdirSync('./skills');
   
   // 检查ckawhub（假设有API）
   const ckawhubSkills = await checkCkawhub(skillName);
   
   if (localSkills.includes(skillName) || ckawhubSkills.includes(skillName)) {
     // 生成替代名称或提示用户
   }
   ```

2. **生成SKILL.md**
   - 包含YAML前置信息（name, description, license）
   - 详细的功能说明
   - 使用方法和示例代码
   - 论文参考信息

3. **创建辅助文件**
   - scripts/目录下的示例脚本
   - 必要的配置文件
   - LICENSE文件

4. **编写使用案例**
   - 模拟用户问题场景
   - 展示skill的完整调用流程
   - 预期输出示例

## SKILL.md模板

生成的skill文件遵循以下模板：

```markdown
---
name: [skill-name]
description: "[简洁描述skill的功能和适用场景]"
license: MIT
---

# [Skill Name]

[skill的详细介绍]

## 核心能力

[列出skill的主要功能]

## 使用方法

### 基本用法

[示例代码]

### 高级用法

[进阶示例]

## 参考论文

本skill基于以下论文的核心方法论开发：

- **标题**：[论文标题]
- **作者**：[作者]
- **链接**：[arXiv/DOI链接]
- **核心贡献**：[简述论文贡献]

## 使用案例

### 案例1：[场景描述]

**用户问题**：[模拟用户输入]

**Skill响应**：[展示skill如何处理]

## 注意事项

[使用skill时需要注意的事项]
```

## 论文参考信息格式

每个生成的skill必须包含完整的论文参考信息：

```markdown
## 学术参考

### 主要参考论文
- **标题**：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **作者**：Jason Wei, Xuezhi Wang, et al.
- **机构**：Google Research
- **发表**：NeurIPS 2022
- **链接**：https://arxiv.org/abs/2201.11903
- **引用数**：3000+ (截至2024年)

### 方法论来源
本skill的核心方法来源于上述论文的第3节"Chain-of-Thought Prompting"，
将论文提出的思维链推理方法转化为可复用的AI能力。

### 相关论文
1. [相关论文1]
2. [相关论文2]
```

## 使用案例示例

### 案例：从Chain-of-Thought论文生成Skill

**用户请求**：
> "帮我分析Chain-of-Thought那篇论文，生成一个skill"

**执行过程**：

1. **搜索论文**
   ```
   搜索 "Chain-of-Thought Prompting arxiv"
   找到：https://arxiv.org/abs/2201.11903
   ```

2. **分析论文**
   ```
   核心方法：通过逐步推理提示激发LLM的推理能力
   思维模式：将复杂问题分解为中间推理步骤
   创新点：无需微调，仅通过prompt设计提升推理能力
   ```

3. **检测命名冲突**
   ```
   本地skills目录：未找到 "chain-of-thought"
   ckawhub：未找到同名skill
   可以使用名称：chain-of-thought
   ```

4. **生成Skill**
   - 创建 `/skills/chain-of-thought/SKILL.md`
   - 包含完整的使用说明和示例

5. **输出结果**
   ```
   ✅ Skill生成成功！
   📁 位置：/skills/chain-of-thought/SKILL.md
   📄 参考论文：Chain-of-Thought Prompting Elicits Reasoning...
   🔗 论文链接：https://arxiv.org/abs/2201.11903
   ```

### 案例：自动发现热门论文生成Skill

**用户请求**：
> "自动发现最近一周NLP领域的热门论文，生成一个skill"

**执行过程**：

1. **搜索热门论文**
   ```
   搜索 arXiv NLP recent popular papers
   发现候选：
   1. "LoRA: Low-Rank Adaptation" - 引用数高，热度持续
   2. "QLoRA: Efficient Finetuning" - 最新热点
   3. ...
   ```

2. **选择最佳论文**
   ```
   基于综合评分选择：QLoRA
   理由：最新、高关注度、实用性强
   ```

3. **分析并生成Skill**
   ```
   生成skill：qlora-finetuning
   功能：高效的量化微调指南
   ```

## API参数说明

### paper_to_skill 函数参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| action | string | 是 | 操作类型：auto_discover, generate_from_url, analyze_only |
| field | string | 否 | 研究领域（用于auto_discover） |
| days | number | 否 | 搜索最近N天的论文（默认7天） |
| paper_url | string | 条件 | 论文URL（generate_from_url和analyze_only必需） |
| skill_name | string | 否 | 自定义skill名称（可选，默认自动生成） |
| output_dir | string | 否 | skill输出目录（默认./skills） |

## 最佳实践

### 1. 论文选择建议
- 优先选择方法论清晰、可操作性强的论文
- 避免选择纯理论、难以实现的论文
- 关注工业界广泛采用的论文

### 2. Skill命名规范
- 使用小写字母和连字符
- 名称应反映核心功能
- 避免与现有skill重名

### 3. 文档完整性
- 必须包含论文参考信息
- 提供清晰的使用示例
- 说明skill的局限性

## 注意事项

1. **版权尊重**：生成的skill应基于论文的方法论思想，而非直接复制论文内容
2. **引用规范**：必须在skill中注明参考论文的完整信息
3. **质量把控**：不是所有论文都适合转化为skill，需要评估实用性
4. **持续更新**：论文可能有更新版本，skill也应相应更新

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 找不到论文 | 检查URL是否正确，或使用论文标题搜索 |
| 命名冲突 | 使用skill_name参数指定新名称 |
| 分析失败 | 论文可能太新或格式特殊，尝试手动分析 |
| 生成不完整 | 检查论文是否有完整的方法论描述 |

## 相关Skills

- `web-search`: 用于搜索论文
- `web-reader`: 用于读取论文网页内容
- `pdf`: 用于解析PDF格式的论文
- `LLM`: 用于论文内容分析和skill生成
