# Paper-to-Skill 使用案例

本文档详细展示 `paper-to-skill` skill 的完整使用流程和预期效果。

## 案例1：自动发现热门论文生成Skill

### 用户请求

```
用户：帮我自动发现最近一周NLP领域的热门论文，生成一个skill
```

### 执行流程

#### 步骤1：搜索热门论文

Skill 首先使用 web-search 搜索 NLP 领域的热门论文：

```javascript
// 搜索查询
const queries = [
  "site:arxiv.org NLP trending papers 2024",
  "NLP breakthrough research high citations recent",
  "best NLP papers NeurIPS ICML ICLR 2024"
];
```

**搜索结果示例**：

```json
[
  {
    "title": "LoRA: Low-Rank Adaptation of Large Language Models",
    "url": "https://arxiv.org/abs/2106.09685",
    "citations": 5000,
    "relevanceScore": 0.92
  },
  {
    "title": "QLoRA: Efficient Finetuning of Quantized LLMs",
    "url": "https://arxiv.org/abs/2305.14314",
    "citations": 2000,
    "relevanceScore": 0.88
  },
  {
    "title": "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
    "url": "https://arxiv.org/abs/2201.11903",
    "citations": 3000,
    "relevanceScore": 0.85
  }
]
```

#### 步骤2：选择最佳论文

基于综合评分，选择 `QLoRA: Efficient Finetuning of Quantized LLMs`：
- 最新发表（2023年5月）
- 高引用数（2000+）
- 实用性强（高效的微调方法）
- 工业界广泛关注

#### 步骤3：分析论文

Skill 使用 LLM 深度分析论文：

**分析结果**：

```markdown
## 基本信息
- 标题：QLoRA: Efficient Finetuning of Quantized LLMs
- 作者：Tim Dettmers, Artidoro Pagnoni, et al.
- 发表时间：2023年5月
- 来源：arXiv

## 核心方法论
QLoRA 提出了一种高效的量化微调方法：
1. 4-bit NormalFloat (NF4) 量化：新的数据类型，更适合正态分布的权重
2. 双重量化：对量化常数再次量化，进一步减少内存
3. 分页优化器：使用 NVIDIA 统一内存避免 GPU 内存溢出

## 思维框架
- 问题分解：将大模型微调的内存瓶颈分解为量化精度和内存管理两个子问题
- 渐进优化：从标准量化 → 更优数据类型 → 双重量化 → 分页管理
- 实用导向：保持与 LoRA 相同的性能，但大幅降低资源需求

## 创新点
1. 提出 NF4 数据类型，量化精度更高
2. 双重量化技术，额外节省 0.5 bits/参数
3. 分页优化器，处理长序列时的内存峰值
4. 在 48GB GPU 上微调 65B 参数模型

## Skill转化建议
- 建议skill名称：qlora-finetuning
- 核心功能描述：高效量化微调大语言模型的完整指南
- 适用场景：
  - 资源受限环境下微调大模型
  - 快速实验不同微调配置
  - 学习量化微调最佳实践

## 实用性评分
9/10
```

#### 步骤4：检测命名冲突

```javascript
// 检查本地skills目录
const localSkills = fs.readdirSync('./skills');
// 结果：未找到 "qlora-finetuning"

// 检查ckawhub（假设）
// 结果：未找到同名skill

// 结论：可以使用名称 "qlora-finetuning"
```

#### 步骤5：生成Skill

创建以下文件结构：

```
skills/
└── qlora-finetuning/
    ├── SKILL.md
    ├── LICENSE.txt
    └── scripts/
        └── example.ts
```

**生成的 SKILL.md 内容**：

```markdown
---
name: qlora-finetuning
description: "高效量化微调大语言模型的完整指南，基于QLoRA论文方法论"
license: MIT
---

# QLoRA Finetuning

高效量化微调大语言模型的完整指南，基于QLoRA论文方法论

## 核心能力

本skill基于论文"QLoRA: Efficient Finetuning of Quantized LLMs"的核心方法论，提供以下能力：

- 资源受限环境下微调大模型
- 快速实验不同微调配置
- 学习量化微调最佳实践

## 使用方法

### 基本用法

```javascript
// 调用示例
const result = await useSkill('qlora-finetuning', {
  input: '你的输入内容'
});
console.log(result);
```

### 详细说明

QLoRA 提出了一种高效的量化微调方法：
1. 4-bit NormalFloat (NF4) 量化：新的数据类型，更适合正态分布的权重
2. 双重量化：对量化常数再次量化，进一步减少内存
3. 分页优化器：使用 NVIDIA 统一内存避免 GPU 内存溢出

## 思维框架

- 问题分解：将大模型微调的内存瓶颈分解为量化精度和内存管理两个子问题
- 渐进优化：从标准量化 → 更优数据类型 → 双重量化 → 分页管理
- 实用导向：保持与 LoRA 相同的性能，但大幅降低资源需求

## 创新点

1. 提出 NF4 数据类型，量化精度更高
2. 双重量化技术，额外节省 0.5 bits/参数
3. 分页优化器，处理长序列时的内存峰值
4. 在 48GB GPU 上微调 65B 参数模型

## 参考论文

本skill基于以下学术论文的核心方法论开发：

### 主要参考论文

| 项目 | 内容 |
|------|------|
| **标题** | QLoRA: Efficient Finetuning of Quantized LLMs |
| **作者** | Tim Dettmers, Artidoro Pagnoni, et al. |
| **发表时间** | 2023年5月 |
| **来源** | arXiv |
| **链接** | [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314) |

### 方法论来源

本skill的核心方法来源于上述论文，将论文提出的方法论转化为可复用的AI能力。

## 使用案例

### 案例1：基础使用场景

**用户问题**：我有一块24GB显存的GPU，想微调Llama-2-70B，可行吗？

**Skill响应**：
```
根据QLoRA方法论，这是可行的！

关键配置：
1. 使用4-bit NF4量化：将70B模型压缩到约35GB
2. 启用双重量化：进一步节省约3.5GB
3. 使用分页优化器：处理内存峰值

实际内存需求：
- 模型权重：~35GB（4-bit量化后）
- 梯度+优化器：~8GB（LoRA只训练少量参数）
- 激活值：~5GB（使用gradient checkpointing）

总计约48GB，24GB显存需要使用CPU offload或选择更小的模型。

建议：使用Llama-2-13B或Llama-2-34B，在24GB显存上可以完全放入GPU。
```

### 案例2：进阶应用场景

**用户问题**：如何选择QLoRA的最佳配置参数？

**Skill响应**：
```
根据论文实验结果，推荐以下配置：

1. 量化类型：NF4（论文提出的新数据类型）
2. 双重量化：启用（节省额外内存）
3. LoRA rank：16-64（平衡性能和内存）
4. LoRA alpha：rank的2倍
5. 目标模块：q_proj, v_proj, k_proj, o_proj

代码示例：
```python
from peft import LoraConfig, get_peft_model
from transformers import BitsAndBytesConfig

# QLoRA配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

# LoRA配置
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none"
)
```
```

## 注意事项

1. 本skill基于学术论文方法论，实际效果可能因应用场景而异
2. 建议在使用前阅读原论文以深入理解方法原理
3. 如需引用，请引用原论文

## 更新日志

- **2024-01-15**: 初始版本，基于论文"QLoRA: Efficient Finetuning of Quantized LLMs"生成
```

#### 步骤6：输出结果

```
✅ Skill生成成功！

📁 位置：/skills/qlora-finetuning/SKILL.md
📄 参考论文：QLoRA: Efficient Finetuning of Quantized LLMs
🔗 论文链接：https://arxiv.org/abs/2305.14314
📊 实用性评分：9/10

生成的文件：
├── SKILL.md (主文件)
├── LICENSE.txt (MIT许可证)
└── scripts/
    └── example.ts (示例脚本)
```

---

## 案例2：从指定论文URL生成Skill

### 用户请求

```
用户：帮我分析这篇论文 https://arxiv.org/abs/2201.11903 并生成一个skill
```

### 执行流程

#### 步骤1：获取论文内容

使用 web-reader 获取论文页面内容。

#### 步骤2：分析论文

**分析结果**：

```markdown
## 基本信息
- 标题：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- 作者：Jason Wei, Xuezhi Wang, Dale Schuurmans, et al.
- 发表时间：2022年1月
- 来源：arXiv (NeurIPS 2022)

## 核心方法论
Chain-of-Thought (CoT) 提示是一种通过生成中间推理步骤来增强大语言模型推理能力的技术：
1. 在提示中包含示例的推理过程
2. 引导模型逐步分解复杂问题
3. 通过中间步骤提高最终答案的准确性

## 思维框架
- 问题分解：将复杂问题分解为可管理的子问题
- 显式推理：要求模型展示推理过程而非直接给出答案
- 示例学习：通过少量示例教会模型推理模式

## 创新点
1. 无需微调，仅通过提示设计提升推理能力
2. 在数学推理、常识推理等任务上显著提升
3. 模型规模越大，CoT效果越明显
4. 提出了"涌现能力"的概念

## Skill转化建议
- 建议skill名称：chain-of-thought
- 核心功能描述：通过思维链提示增强AI推理能力
- 适用场景：
  - 复杂数学问题求解
  - 多步骤逻辑推理
  - 需要解释推理过程的场景

## 实用性评分
10/10
```

#### 步骤3：检测命名冲突

```javascript
// 检查本地skills目录
// 结果：未找到 "chain-of-thought"

// 检查ckawhub
// 结果：未找到同名skill

// 结论：可以使用名称 "chain-of-thought"
```

#### 步骤4：生成Skill

创建完整的 skill 文件结构。

#### 步骤5：输出结果

```
✅ Skill生成成功！

📁 位置：/skills/chain-of-thought/SKILL.md
📄 参考论文：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
🔗 论文链接：https://arxiv.org/abs/2201.11903
📊 实用性评分：10/10
```

---

## 案例3：仅分析论文（预览模式）

### 用户请求

```
用户：帮我分析这篇论文 https://arxiv.org/abs/2303.08774，但不要生成skill
```

### 执行流程

Skill 只执行分析步骤，输出分析报告，不创建 skill 文件。

**输出结果**：

```markdown
## 论文分析报告

### 基本信息
- 标题：GPT-4 Technical Report
- 作者：OpenAI
- 发表时间：2023年3月
- 来源：arXiv

### 核心方法论
GPT-4 是一个大规模多模态模型，能够接受图像和文本输入并生成文本输出：
1. 大规模预训练：在大量文本和图像数据上训练
2. 人类反馈强化学习（RLHF）：对齐模型行为与人类意图
3. 可预测的扩展性：训练过程可以预测最终性能

### 思维框架
- 多模态融合：统一处理文本和图像
- 渐进式能力：从小模型预测大模型性能
- 安全对齐：将安全考虑融入训练过程

### 创新点
1. 多模态输入能力
2. 在专业考试中达到人类水平
3. 可预测的扩展规律
4. 改进的安全性和对齐

### Skill转化建议
- 建议skill名称：gpt4-multimodal
- 核心功能描述：多模态AI能力应用指南
- 适用场景：
  - 图像理解与分析
  - 复杂推理任务
  - 专业领域问答

### 实用性评分
7/10（模型本身不开放，但方法论可借鉴）

### 分析结论
该论文适合作为参考学习材料，但由于GPT-4模型不开放，转化为skill的实用性有限。
建议关注其方法论和实验设计思路。
```

---

## 案例4：命名冲突处理

### 用户请求

```
用户：从 https://arxiv.org/abs/2106.09685 生成一个叫 "lora" 的skill
```

### 执行流程

#### 步骤1：检测命名冲突

```javascript
// 检查本地skills目录
const localSkills = fs.readdirSync('./skills');
// 假设结果：发现 "lora" 目录已存在

// 返回冲突信息
{
  exists: true,
  location: '本地skills目录'
}
```

#### 步骤2：提示用户或自动生成新名称

**选项A：提示用户**

```
❌ Skill名称 "lora" 已存在于本地skills目录

建议的替代名称：
1. lora-v2
2. lora-adaptation
3. low-rank-adaptation

请选择一个名称或提供自定义名称：
```

**选项B：自动生成**

```javascript
// 自动生成唯一名称
const uniqueName = await generateUniqueSkillName('lora');
// 结果：'lora-v2'（如果lora已存在）
```

#### 步骤3：使用新名称生成Skill

```
✅ 使用名称 "lora-v2" 生成skill成功！

📁 位置：/skills/lora-v2/SKILL.md
📄 参考论文：LoRA: Low-Rank Adaptation of Large Language Models
```

---

## 总结

`paper-to-skill` skill 提供了三种主要使用模式：

| 模式 | 命令 | 适用场景 |
|------|------|----------|
| 自动发现 | `auto_discover` | 探索领域最新进展，自动选择最佳论文 |
| 指定URL | `generate_from_url` | 已知论文，需要转化为skill |
| 仅分析 | `analyze_only` | 评估论文价值，预览分析结果 |

生成的每个skill都包含：
- 完整的论文参考信息
- 核心方法论说明
- 思维框架分析
- 使用案例和示例代码
- 注意事项和更新日志
