# Paper-to-Skill: 论文驱动的Skill生成器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个元技能（Meta-Skill），用于从高质量学术论文中自动提取核心方法论，并将其转化为可复用的AI技能。

## 核心功能

- 🔍 **论文发现**：自动搜索arXiv等平台的热门论文
- 📊 **深度分析**：提取论文方法论、思维框架、创新点
- 🛠️ **Skill生成**：自动创建完整的skill文件结构
- ✅ **冲突检测**：检查本地和ckawhub的命名冲突
- 📝 **案例生成**：提供详细的使用案例和示例代码

## 快速开始

### 安装依赖

```bash
# 确保已安装 z-ai-web-dev-sdk
npm install z-ai-web-dev-sdk
```

### 使用方式

#### 方式一：CLI命令

```bash
# 自动发现热门论文并生成skill
npx ts-node scripts/paper_to_skill.ts auto_discover NLP 7

# 从指定URL生成skill
npx ts-node scripts/paper_to_skill.ts generate_from_url https://arxiv.org/abs/2201.11903

# 仅分析论文
npx ts-node scripts/paper_to_skill.ts analyze_only https://arxiv.org/abs/2305.14314
```

#### 方式二：SDK调用

```javascript
import ZAI from 'z-ai-web-dev-sdk';

async function generateSkill() {
  const zai = await ZAI.create();
  
  // 自动发现并生成
  const result = await zai.functions.invoke('paper_to_skill', {
    action: 'auto_discover',
    field: 'AI',
    days: 7
  });
  
  console.log(result);
}
```

## 工作流程

```
论文搜索 → 论文分析 → 命名检测 → Skill生成 → 案例编写
    ↓           ↓           ↓           ↓           ↓
  arXiv     方法论提取   本地/远程检查  SKILL.md    使用示例
```

## 生成的Skill结构

```
skills/
└── [skill-name]/
    ├── SKILL.md        # 主文件，包含完整说明
    ├── LICENSE.txt     # MIT许可证
    └── scripts/
        └── example.ts  # 示例脚本
```

## SKILL.md模板

每个生成的skill都包含：

1. **YAML前置信息**：name, description, license
2. **核心能力说明**：skill的主要功能
3. **使用方法**：基本用法和高级用法
4. **参考论文**：完整的论文引用信息
5. **使用案例**：模拟用户场景的示例
6. **注意事项**：使用限制和建议

## 示例：从Chain-of-Thought论文生成Skill

**输入**：
```
论文URL: https://arxiv.org/abs/2201.11903
```

**输出**：
```
✅ Skill生成成功！
📁 位置：/skills/chain-of-thought/SKILL.md
📄 参考论文：Chain-of-Thought Prompting Elicits Reasoning...
🔗 论文链接：https://arxiv.org/abs/2201.11903
```

生成的skill可以帮助用户：
- 理解思维链提示的核心原理
- 应用CoT解决复杂推理问题
- 学习如何设计有效的提示

## API参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| action | string | 是 | auto_discover / generate_from_url / analyze_only |
| field | string | 否 | 研究领域（用于auto_discover） |
| days | number | 否 | 搜索最近N天的论文 |
| paper_url | string | 条件 | 论文URL |
| skill_name | string | 否 | 自定义skill名称 |
| output_dir | string | 否 | 输出目录 |

## 最佳实践

1. **论文选择**：优先选择方法论清晰、实用性强的论文
2. **命名规范**：使用小写字母和连字符，名称应反映核心功能
3. **引用规范**：必须在skill中注明参考论文的完整信息
4. **质量把控**：不是所有论文都适合转化为skill

## 注意事项

- 生成的skill基于论文的方法论思想，不直接复制论文内容
- 请尊重论文作者的版权，正确引用原论文
- 建议在使用前阅读原论文以深入理解方法原理

## 相关资源

- [使用案例详解](./USE_CASES.md)
- [arXiv](https://arxiv.org/)
- [Google Scholar](https://scholar.google.com/)

## 许可证

MIT License - 详见 [LICENSE.txt](./LICENSE.txt)
