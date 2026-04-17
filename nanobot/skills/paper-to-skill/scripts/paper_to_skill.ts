/**
 * Paper-to-Skill: 论文驱动的Skill生成器
 * 
 * 这个脚本实现了从学术论文自动生成AI技能的核心逻辑
 */

import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';
import * as path from 'path';

// 类型定义
interface PaperInfo {
  title: string;
  url: string;
  authors?: string[];
  abstract?: string;
  citations?: number;
  publishDate?: string;
  field?: string;
  relevanceScore?: number;
}

interface PaperAnalysis {
  basicInfo: {
    title: string;
    authors: string[];
    publishDate: string;
    source: string;
    url: string;
  };
  methodology: string;
  thinkingPattern: string;
  innovations: string[];
  skillSuggestion: {
    name: string;
    description: string;
    useCases: string[];
  };
  practicalityScore: number;
}

interface SkillGenerateOptions {
  paperUrl?: string;
  field?: string;
  days?: number;
  skillName?: string;
  outputDir?: string;
  action: 'auto_discover' | 'generate_from_url' | 'analyze_only';
}

interface SkillMetadata {
  name: string;
  description: string;
  license: string;
}

// 主类
class PaperToSkillGenerator {
  private zai: any;
  private skillsDir: string;

  constructor(skillsDir: string = './skills') {
    this.skillsDir = skillsDir;
  }

  async initialize() {
    this.zai = await ZAI.create();
  }

  /**
   * 搜索热门论文
   */
  async searchTrendingPapers(field: string, days: number = 7): Promise<PaperInfo[]> {
    const queries = [
      `site:arxiv.org ${field} trending papers 2024`,
      `${field} breakthrough research high citations recent`,
      `best ${field} papers NeurIPS ICML ICLR 2024`
    ];

    const allResults: PaperInfo[] = [];

    for (const query of queries) {
      try {
        const results = await this.zai.functions.invoke('web_search', {
          query: query,
          num: 10
        });

        for (const result of results || []) {
          if (result.url && result.url.includes('arxiv.org')) {
            allResults.push({
              title: result.name,
              url: result.url,
              citations: 0,
              field: field,
              relevanceScore: this.calculateRelevanceScore(result, field)
            });
          }
        }
      } catch (error) {
        console.error(`搜索查询失败: ${query}`, error);
      }
    }

    // 去重并排序
    const uniqueResults = this.deduplicatePapers(allResults);
    return uniqueResults.sort((a, b) => (b.relevanceScore || 0) - (a.relevanceScore || 0));
  }

  /**
   * 计算论文相关性分数
   */
  private calculateRelevanceScore(result: any, field: string): number {
    let score = 0.5; // 基础分

    // 标题相关性
    if (result.name && result.name.toLowerCase().includes(field.toLowerCase())) {
      score += 0.2;
    }

    // 来源权威性
    if (result.url && result.url.includes('arxiv.org')) {
      score += 0.1;
    }

    // 摘要质量
    if (result.snippet && result.snippet.length > 100) {
      score += 0.1;
    }

    // 时间因素（新论文加分）
    if (result.date) {
      const resultDate = new Date(result.date);
      const now = new Date();
      const daysDiff = (now.getTime() - resultDate.getTime()) / (1000 * 60 * 60 * 24);
      if (daysDiff < 30) {
        score += 0.1;
      }
    }

    return Math.min(score, 1.0);
  }

  /**
   * 论文去重
   */
  private deduplicatePapers(papers: PaperInfo[]): PaperInfo[] {
    const seen = new Set<string>();
    return papers.filter(paper => {
      const key = paper.url || paper.title;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  /**
   * 获取论文详细内容
   */
  async fetchPaperContent(paperUrl: string): Promise<string> {
    try {
      // 使用web-reader获取论文页面内容
      const content = await this.zai.functions.invoke('web_reader', {
        url: paperUrl
      });
      return content;
    } catch (error) {
      console.error('获取论文内容失败:', error);
      return '';
    }
  }

  /**
   * 分析论文
   */
  async analyzePaper(paperUrl: string, paperContent?: string): Promise<PaperAnalysis> {
    // 如果没有提供内容，先获取
    if (!paperContent) {
      paperContent = await this.fetchPaperContent(paperUrl);
    }

    // 使用LLM分析论文
    const analysisPrompt = `你是一位学术研究专家。请分析以下论文内容，提取关键信息。

论文URL: ${paperUrl}

论文内容:
${paperContent || '(内容获取失败，请基于URL推断)'}

请按以下格式输出分析结果：

## 基本信息
- 标题：[论文标题]
- 作者：[作者列表]
- 发表时间：[日期]
- 来源：[arXiv/会议/期刊]

## 核心方法论
[详细描述论文的核心方法，包括算法、模型、流程等]

## 思维框架
[描述论文解决问题的思维方式，如何分解问题、如何推理]

## 创新点
1. [创新点1]
2. [创新点2]
3. [创新点3]

## Skill转化建议
- 建议skill名称：[英文小写，用连字符连接]
- 核心功能描述：[一句话描述]
- 适用场景：[列出3-5个使用场景]

## 实用性评分
[1-10分，评估该方法转化为AI skill的可行性]

请确保输出格式规范，内容详实。`;

    const completion = await this.zai.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: '你是一位资深的学术研究专家和AI技能设计师，擅长分析学术论文并将其转化为实用的AI能力。'
        },
        {
          role: 'user',
          content: analysisPrompt
        }
      ],
      thinking: { type: 'disabled' }
    });

    const analysisText = completion.choices[0]?.message?.content || '';
    
    // 解析分析结果
    return this.parseAnalysisResult(analysisText, paperUrl);
  }

  /**
   * 解析分析结果
   */
  private parseAnalysisResult(analysisText: string, paperUrl: string): PaperAnalysis {
    // 简单的解析逻辑，实际应用中可以使用更复杂的解析
    const extractSection = (text: string, sectionName: string): string => {
      const regex = new RegExp(`## ${sectionName}[\\s\\S]*?(?=## |$)`, 'i');
      const match = text.match(regex);
      return match ? match[0].replace(new RegExp(`## ${sectionName}`, 'i'), '').trim() : '';
    };

    const basicInfoSection = extractSection(analysisText, '基本信息');
    const methodologySection = extractSection(analysisText, '核心方法论');
    const thinkingSection = extractSection(analysisText, '思维框架');
    const innovationsSection = extractSection(analysisText, '创新点');
    const suggestionSection = extractSection(analysisText, 'Skill转化建议');
    const scoreSection = extractSection(analysisText, '实用性评分');

    // 提取基本信息
    const titleMatch = basicInfoSection.match(/标题[：:]\s*(.+)/);
    const authorsMatch = basicInfoSection.match(/作者[：:]\s*(.+)/);
    const dateMatch = basicInfoSection.match(/发表时间[：:]\s*(.+)/);
    const sourceMatch = basicInfoSection.match(/来源[：:]\s*(.+)/);

    // 提取创新点
    const innovations = innovationsSection
      .split(/\n/)
      .filter(line => line.match(/^\d+\./))
      .map(line => line.replace(/^\d+\.\s*/, '').trim());

    // 提取skill建议
    const nameMatch = suggestionSection.match(/skill名称[：:]\s*(.+)/i);
    const descMatch = suggestionSection.match(/功能描述[：:]\s*(.+)/i);
    const useCasesMatch = suggestionSection.match(/适用场景[：:]\s*(.+)/i);

    // 提取评分
    const scoreMatch = scoreSection.match(/(\d+)/);
    const practicalityScore = scoreMatch ? parseInt(scoreMatch[1]) : 5;

    return {
      basicInfo: {
        title: titleMatch ? titleMatch[1].trim() : '未知标题',
        authors: authorsMatch ? authorsMatch[1].split(/[,，、]/).map(a => a.trim()) : [],
        publishDate: dateMatch ? dateMatch[1].trim() : '未知日期',
        source: sourceMatch ? sourceMatch[1].trim() : 'arXiv',
        url: paperUrl
      },
      methodology: methodologySection,
      thinkingPattern: thinkingSection,
      innovations: innovations.length > 0 ? innovations : ['创新点提取失败'],
      skillSuggestion: {
        name: nameMatch ? nameMatch[1].trim().toLowerCase().replace(/\s+/g, '-') : 'unnamed-skill',
        description: descMatch ? descMatch[1].trim() : '',
        useCases: useCasesMatch ? useCasesMatch[1].split(/[;；]/).map(u => u.trim()) : []
      },
      practicalityScore: practicalityScore
    };
  }

  /**
   * 检查skill命名冲突
   */
  async checkNamingConflict(skillName: string): Promise<{ exists: boolean; location?: string }> {
    // 检查本地skills目录
    const localSkillPath = path.join(this.skillsDir, skillName);
    if (fs.existsSync(localSkillPath)) {
      return { exists: true, location: '本地skills目录' };
    }

    // 检查ckawhub（模拟，实际需要API）
    // const ckawhubExists = await this.checkCkawhub(skillName);
    // if (ckawhubExists) {
    //   return { exists: true, location: 'ckawhub' };
    // }

    return { exists: false };
  }

  /**
   * 生成唯一的skill名称
   */
  async generateUniqueSkillName(baseName: string): Promise<string> {
    let skillName = baseName;
    let counter = 1;

    while (true) {
      const conflict = await this.checkNamingConflict(skillName);
      if (!conflict.exists) {
        return skillName;
      }
      skillName = `${baseName}-v${counter}`;
      counter++;
    }
  }

  /**
   * 生成SKILL.md内容
   */
  generateSkillMarkdown(analysis: PaperAnalysis): string {
    const { basicInfo, methodology, thinkingPattern, innovations, skillSuggestion } = analysis;

    return `---
name: ${skillSuggestion.name}
description: "${skillSuggestion.description}"
license: MIT
---

# ${this.formatSkillName(skillSuggestion.name)}

${skillSuggestion.description}

## 核心能力

本skill基于论文"${basicInfo.title}"的核心方法论，提供以下能力：

${this.formatUseCases(skillSuggestion.useCases)}

## 使用方法

### 基本用法

\`\`\`javascript
// 调用示例
const result = await useSkill('${skillSuggestion.name}', {
  input: '你的输入内容'
});
console.log(result);
\`\`\`

### 详细说明

${methodology}

## 思维框架

${thinkingPattern}

## 创新点

${innovations.map((inn, i) => `${i + 1}. ${inn}`).join('\n')}

## 参考论文

本skill基于以下学术论文的核心方法论开发：

### 主要参考论文

| 项目 | 内容 |
|------|------|
| **标题** | ${basicInfo.title} |
| **作者** | ${basicInfo.authors.join(', ')} |
| **发表时间** | ${basicInfo.publishDate} |
| **来源** | ${basicInfo.source} |
| **链接** | [${basicInfo.url}](${basicInfo.url}) |

### 方法论来源

本skill的核心方法来源于上述论文，将论文提出的方法论转化为可复用的AI能力。

## 使用案例

### 案例1：基础使用场景

**用户问题**：请帮我使用${skillSuggestion.name}方法分析这个问题...

**Skill响应**：
\`\`\`
[展示skill如何处理该问题]
\`\`\`

### 案例2：进阶应用场景

**用户问题**：如何将${skillSuggestion.name}应用到更复杂的场景？

**Skill响应**：
\`\`\`
[展示进阶用法]
\`\`\`

## 注意事项

1. 本skill基于学术论文方法论，实际效果可能因应用场景而异
2. 建议在使用前阅读原论文以深入理解方法原理
3. 如需引用，请引用原论文

## 更新日志

- **${new Date().toISOString().split('T')[0]}**: 初始版本，基于论文"${basicInfo.title}"生成
`;
  }

  /**
   * 格式化skill名称
   */
  private formatSkillName(name: string): string {
    return name
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  /**
   * 格式化使用场景
   */
  private formatUseCases(useCases: string[]): string {
    if (useCases.length === 0) {
      return '- 通用AI辅助能力';
    }
    return useCases.map(uc => `- ${uc}`).join('\n');
  }

  /**
   * 创建skill目录和文件
   */
  async createSkill(analysis: PaperAnalysis, outputDir?: string): Promise<string> {
    const skillName = analysis.skillSuggestion.name;
    const targetDir = outputDir || this.skillsDir;
    const skillDir = path.join(targetDir, skillName);

    // 创建目录
    if (!fs.existsSync(skillDir)) {
      fs.mkdirSync(skillDir, { recursive: true });
    }

    // 创建scripts子目录
    const scriptsDir = path.join(skillDir, 'scripts');
    if (!fs.existsSync(scriptsDir)) {
      fs.mkdirSync(scriptsDir, { recursive: true });
    }

    // 生成SKILL.md
    const skillMdContent = this.generateSkillMarkdown(analysis);
    fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillMdContent, 'utf-8');

    // 创建LICENSE文件
    const licenseContent = `MIT License

Copyright (c) ${new Date().getFullYear()}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
`;
    fs.writeFileSync(path.join(skillDir, 'LICENSE.txt'), licenseContent, 'utf-8');

    // 创建示例脚本
    const exampleScript = `/**
 * ${analysis.skillSuggestion.name} skill 示例脚本
 * 
 * 基于论文: ${analysis.basicInfo.title}
 */

// 示例使用方法
async function example() {
  console.log('使用 ${analysis.skillSuggestion.name} skill');
  // TODO: 实现具体功能
}

export { example };
`;
    fs.writeFileSync(path.join(scriptsDir, 'example.ts'), exampleScript, 'utf-8');

    return skillDir;
  }

  /**
   * 主入口：自动发现论文并生成skill
   */
  async autoDiscoverAndGenerate(field: string, days: number = 7, outputDir?: string): Promise<{
    success: boolean;
    skillPath?: string;
    paperInfo?: PaperInfo;
    analysis?: PaperAnalysis;
    message: string;
  }> {
    console.log(`正在搜索 ${field} 领域最近 ${days} 天的热门论文...`);

    // 搜索论文
    const papers = await this.searchTrendingPapers(field, days);
    
    if (papers.length === 0) {
      return {
        success: false,
        message: `未找到 ${field} 领域的热门论文`
      };
    }

    console.log(`找到 ${papers.length} 篇候选论文，正在分析最佳论文...`);

    // 选择最佳论文
    const selectedPaper = papers[0];
    console.log(`选择论文: ${selectedPaper.title}`);

    // 分析论文
    const analysis = await this.analyzePaper(selectedPaper.url);

    // 检查命名冲突并生成唯一名称
    const uniqueName = await this.generateUniqueSkillName(analysis.skillSuggestion.name);
    analysis.skillSuggestion.name = uniqueName;

    // 创建skill
    const skillPath = await this.createSkill(analysis, outputDir);

    return {
      success: true,
      skillPath,
      paperInfo: selectedPaper,
      analysis,
      message: `成功生成skill: ${uniqueName}`
    };
  }

  /**
   * 从指定URL生成skill
   */
  async generateFromUrl(paperUrl: string, skillName?: string, outputDir?: string): Promise<{
    success: boolean;
    skillPath?: string;
    analysis?: PaperAnalysis;
    message: string;
  }> {
    console.log(`正在分析论文: ${paperUrl}`);

    // 分析论文
    const analysis = await this.analyzePaper(paperUrl);

    // 如果指定了skill名称，使用指定的名称
    if (skillName) {
      const conflict = await this.checkNamingConflict(skillName);
      if (conflict.exists) {
        return {
          success: false,
          message: `Skill名称 "${skillName}" 已存在于${conflict.location}`
        };
      }
      analysis.skillSuggestion.name = skillName;
    } else {
      // 生成唯一名称
      const uniqueName = await this.generateUniqueSkillName(analysis.skillSuggestion.name);
      analysis.skillSuggestion.name = uniqueName;
    }

    // 创建skill
    const skillPath = await this.createSkill(analysis, outputDir);

    return {
      success: true,
      skillPath,
      analysis,
      message: `成功生成skill: ${analysis.skillSuggestion.name}`
    };
  }

  /**
   * 仅分析论文，不生成skill
   */
  async analyzeOnly(paperUrl: string): Promise<{
    success: boolean;
    analysis?: PaperAnalysis;
    message: string;
  }> {
    console.log(`正在分析论文: ${paperUrl}`);

    try {
      const analysis = await this.analyzePaper(paperUrl);
      return {
        success: true,
        analysis,
        message: '论文分析完成'
      };
    } catch (error) {
      return {
        success: false,
        message: `分析失败: ${error}`
      };
    }
  }
}

// 导出
export { PaperToSkillGenerator, SkillGenerateOptions, PaperInfo, PaperAnalysis };

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const action = args[0] || 'help';

  const generator = new PaperToSkillGenerator('./skills');
  await generator.initialize();

  switch (action) {
    case 'auto_discover': {
      const field = args[1] || 'AI';
      const days = parseInt(args[2]) || 7;
      const result = await generator.autoDiscoverAndGenerate(field, days);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case 'generate_from_url': {
      const url = args[1];
      const skillName = args[2];
      if (!url) {
        console.error('请提供论文URL');
        process.exit(1);
      }
      const result = await generator.generateFromUrl(url, skillName);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case 'analyze_only': {
      const url = args[1];
      if (!url) {
        console.error('请提供论文URL');
        process.exit(1);
      }
      const result = await generator.analyzeOnly(url);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    default:
      console.log(`
Paper-to-Skill: 论文驱动的Skill生成器

用法:
  npx ts-node paper_to_skill.ts <action> [options]

Actions:
  auto_discover <field> [days]    自动发现热门论文并生成skill
  generate_from_url <url> [name]  从指定URL生成skill
  analyze_only <url>              仅分析论文，不生成skill

示例:
  npx ts-node paper_to_skill.ts auto_discover NLP 7
  npx ts-node paper_to_skill.ts generate_from_url https://arxiv.org/abs/2201.11903 chain-of-thought
  npx ts-node paper_to_skill.ts analyze_only https://arxiv.org/abs/2201.11903
      `);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main().catch(console.error);
}
