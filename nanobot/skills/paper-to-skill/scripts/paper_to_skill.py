#!/usr/bin/env python3
"""
Paper-to-Skill: 论文驱动的Skill生成器

这个脚本实现了从学术论文自动生成AI技能的核心逻辑
"""

import os
import sys
import json
import re
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import webbrowser
from pathlib import Path

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from web_search import WebSearch
    from sentiment_analyzer import SentimentAnalyzer
except ImportError:
    print("⚠️  依赖模块未找到，将使用基础功能")
    WebSearch = None
    SentimentAnalyzer = None

class PaperToSkillGenerator:
    """论文到技能生成器"""
    
    def __init__(self, skills_dir: str = './skills'):
        self.skills_dir = skills_dir
        self.web_search = WebSearch() if WebSearch else None
        self.sentiment_analyzer = SentimentAnalyzer() if SentimentAnalyzer else None
        
    def search_trending_papers(self, field: str, days: int = 7) -> List[Dict]:
        """搜索热门论文"""
        print(f"🔍 正在搜索 {field} 领域最近 {days} 天的热门论文...")
        
        queries = [
            f'site:arxiv.org {field} trending papers 2024',
            f'{field} breakthrough research high citations recent',
            f'best {field} papers NeurIPS ICML ICLR 2024'
        ]
        
        all_results = []
        
        if self.web_search:
            for query in queries:
                try:
                    print(f"  📝 搜索查询: {query}")
                    results = self.web_search.search(query, count=10)
                    
                    for result in results:
                        if result.get('url') and 'arxiv.org' in result['url']:
                            paper_info = {
                                'title': result.get('name', '未知标题'),
                                'url': result['url'],
                                'authors': [],
                                'abstract': result.get('snippet', ''),
                                'citations': 0,
                                'publish_date': result.get('date', ''),
                                'field': field,
                                'relevance_score': self._calculate_relevance_score(result, field),
                                'tags': [field]
                            }
                            all_results.append(paper_info)
                            
                except Exception as e:
                    print(f"  ❌ 搜索查询失败: {query}, 错误: {e}")
        else:
            # 使用基础搜索
            print("  📝 使用基础搜索功能...")
            fallback_papers = self._get_fallback_papers(field)
            all_results.extend(fallback_papers)
        
        # 去重并排序
        unique_results = self._deduplicate_papers(all_results)
        sorted_results = sorted(unique_results, 
                              key=lambda x: x.get('relevance_score', 0), 
                              reverse=True)
        
        print(f"✅ 找到 {len(sorted_results)} 篇候选论文")
        return sorted_results[:10]  # 返回前10篇
    
    def _calculate_relevance_score(self, result: Dict, field: str) -> float:
        """计算论文相关性分数"""
        score = 0.5  # 基础分
        
        # 标题相关性
        title = result.get('name', '').lower()
        if field.lower() in title:
            score += 0.2
        
        # 来源权威性
        url = result.get('url', '')
        if 'arxiv.org' in url:
            score += 0.1
        
        # 摘要质量
        snippet = result.get('snippet', '')
        if len(snippet) > 100:
            score += 0.1
        
        # 时间因素（新论文加分）
        date_str = result.get('date', '')
        if date_str:
            try:
                # 简单的日期解析
                if '2024' in date_str or '2023' in date_str:
                    score += 0.1
            except:
                pass
        
        return min(score, 1.0)
    
    def _get_fallback_papers(self, field: str) -> List[Dict]:
        """获取备用论文列表（当网络搜索不可用时）"""
        fallback_papers = {
            'AI/ML': [
                {
                    'title': 'Attention Is All You Need',
                    'url': 'https://arxiv.org/abs/1706.03762',
                    'authors': ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar'],
                    'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...',
                    'citations': 50000,
                    'publish_date': '2017',
                    'field': 'AI/ML',
                    'relevance_score': 0.95,
                    'tags': ['Transformer', 'NLP', 'Attention']
                },
                {
                    'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
                    'url': 'https://arxiv.org/abs/1810.04805',
                    'authors': ['Jacob Devlin', 'Ming-Wei Chang', 'Kenton Lee', 'Kristina Toutanova'],
                    'abstract': 'We introduce a new language representation model called BERT...',
                    'citations': 30000,
                    'publish_date': '2018',
                    'field': 'AI/ML',
                    'relevance_score': 0.90,
                    'tags': ['BERT', 'NLP', 'Pre-training']
                }
            ],
            'NLP': [
                {
                    'title': 'GPT-3: Language Models are Few-Shot Learners',
                    'url': 'https://arxiv.org/abs/2005.14165',
                    'authors': ['Tom B. Brown', 'Benjamin Mann', 'Nick Ryder', 'Meric I. Neumann'],
                    'abstract': 'We trained a large language model called GPT-3 with 175 billion parameters...',
                    'citations': 10000,
                    'publish_date': '2020',
                    'field': 'NLP',
                    'relevance_score': 0.92,
                    'tags': ['GPT-3', 'Language Model', 'Few-shot']
                }
            ],
            'Computer Vision': [
                {
                    'title': 'ImageNet Classification with Deep Convolutional Neural Networks',
                    'url': 'https://arxiv.org/abs/1209.5299',
                    'authors': ['Alex Krizhevsky', 'Ilya Sutskever', 'Geoffrey E. Hinton'],
                    'abstract': 'We trained a large, deep convolutional neural network...',
                    'citations': 80000,
                    'publish_date': '2012',
                    'field': 'Computer Vision',
                    'relevance_score': 0.88,
                    'tags': ['CNN', 'ImageNet', 'Deep Learning']
                }
            ]
        }
        
        return fallback_papers.get(field, [])
    
    def _deduplicate_papers(self, papers: List[Dict]) -> List[Dict]:
        """论文去重"""
        seen_urls = set()
        unique_papers = []
        
        for paper in papers:
            url = paper.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_papers.append(paper)
        
        return unique_papers
    
    def fetch_paper_content(self, paper_url: str) -> str:
        """获取论文内容"""
        try:
            print(f"📄 正在获取论文内容: {paper_url}")
            
            # 尝试使用web_fetch
            if hasattr(self, 'web_fetch'):
                content = self.web_fetch(paper_url, maxChars=5000)
                return content
            
            # 基础HTTP请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(paper_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 提取主要内容
            if 'arxiv.org' in paper_url:
                # 对于arXiv论文，尝试提取摘要
                content = response.text
                abstract_match = re.search(r'abstract\s*=\s*"([^"]*)"', content, re.IGNORECASE)
                if abstract_match:
                    return f"论文摘要: {abstract_match.group(1)}"
            
            return response.text[:2000]  # 返回前2000字符
            
        except Exception as e:
            print(f"❌ 获取论文内容失败: {e}")
            return f"内容获取失败: {e}"
    
    def analyze_paper(self, paper_url: str, paper_content: Optional[str] = None) -> Dict:
        """分析论文"""
        print(f"🔍 正在分析论文: {paper_url}")
        
        # 如果没有提供内容，先获取
        if not paper_content:
            paper_content = self.fetch_paper_content(paper_url)
        
        # 使用LLM分析论文（这里用模拟分析）
        analysis_prompt = f"""请分析以下论文内容，提取关键信息：

论文URL: {paper_url}

论文内容:
{paper_content or '(内容获取失败，请基于URL推断)'}

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
[1-10分，评估该方法转化为AI skill的可行性]"""

        # 模拟分析结果（实际应用中应该调用LLM）
        analysis_result = self._simulate_analysis(paper_url, paper_content)
        
        return analysis_result
    
    def _simulate_analysis(self, paper_url: str, paper_content: str) -> Dict:
        """模拟论文分析结果（实际应用中应该调用LLM）"""
        # 基于URL推断论文信息
        url_lower = paper_url.lower()

        if '1706.03762' in url_lower or 'attention-is-all-you-need' in url_lower:
            return {
                'basic_info': {
                    'title': 'Attention Is All You Need',
                    'authors': ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'Jakob Uszkoreit', 'Llion Jones', 'Aidan N. Gomez', 'Łukasz Kaiser', 'Illia Polosukhin'],
                    'publish_date': '2017',
                    'source': 'arXiv',
                    'url': paper_url
                },
                'methodology': 'Transformer模型完全基于注意力机制，摒弃了传统的RNN和CNN结构。模型包含编码器和解码器，每个都由6层相同的层组成。每层包含两个子层：多头注意力机制和前馈神经网络。',
                'thinking_pattern': '将序列建模问题转化为注意力计算问题，通过查询、键、值三个向量的点积来计算注意力权重，实现了并行计算和长距离依赖建模。',
                'innovations': [
                    '提出自注意力机制，允许序列中的每个位置都关注所有位置',
                    '使用多头注意力同时关注不同位置的不同表示子空间',
                    '完全基于注意力机制，摒弃了循环和卷积结构',
                    '实现了高效的并行计算'
                ],
                'skill_suggestion': {
                    'name': 'attention-mechanism',
                    'description': '实现Transformer注意力机制的核心算法，支持多头注意力、自注意力等功能',
                    'use_cases': [
                        '自然语言处理中的序列建模',
                        '机器翻译任务',
                        '文本摘要生成',
                        '问答系统'
                    ]
                },
                'practicality_score': 9
            }
        elif '2303.08774' in url_lower or 'gpt-4' in url_lower:
            return {
                'basic_info': {
                    'title': 'GPT-4 Technical Report',
                    'authors': ['OpenAI'],
                    'publish_date': '2023',
                    'source': 'arXiv',
                    'url': paper_url
                },
                'methodology': 'GPT-4是一个大型语言模型，通过大规模预训练和微调获得。模型采用Transformer架构，使用自回归方式生成文本。在训练过程中使用了多种数据源和优化技术。',
                'thinking_pattern': '基于大规模预训练的语言模型，通过上下文理解和生成能力处理复杂任务。采用自回归生成方式，逐步构建输出结果。',
                'innovations': [
                    '大规模语言模型架构优化',
                    '多模态输入处理能力',
                    '更强的推理和规划能力',
                    '更低的幻觉率'
                ],
                'skill_suggestion': {
                    'name': 'gpt4-technical-report',
                    'description': '基于GPT-4技术报告的skill，提供大语言模型的核心技术和应用方法',
                    'use_cases': [
                        '大语言模型应用开发',
                        '文本生成和处理',
                        '代码生成和解释',
                        '多模态任务处理'
                    ]
                },
                'practicality_score': 9
            }
        elif '2302.13971' in url_lower or 'llama' in url_lower:
            return {
                'basic_info': {
                    'title': 'LLaMA: Open and Efficient Foundation Language Models',
                    'authors': ['Hugo Touvron', 'Louis Martin', 'Kevin Stone', 'Peter Albert', 'Riadh Almazroui', 'Yamini Bhargava', 'Arun Bhargava', 'Sundaram Bhojanapalli'],
                    'publish_date': '2023',
                    'source': 'arXiv',
                    'url': paper_url
                },
                'methodology': 'LLaMA是一个开放的基础语言模型系列，通过调整模型规模、训练数据和优化技术来提升性能。模型使用Transformer架构，支持不同规模的变体。',
                'thinking_pattern': '通过调整模型规模和训练数据来平衡性能和效率，提供可扩展的基础语言模型解决方案。',
                'innovations': [
                    '开放的基础语言模型系列',
                    '高效的模型架构设计',
                    '可扩展的训练策略',
                    '开源社区贡献'
                ],
                'skill_suggestion': {
                    'name': 'llama-foundation-models',
                    'description': '基于LLaMA论文的基础语言模型skill，提供模型架构、训练方法和应用指南',
                    'use_cases': [
                        '基础语言模型开发',
                        '模型微调和部署',
                        '开源模型应用',
                        '模型性能优化'
                    ]
                },
                'practicality_score': 8
            }
        elif '1810.04805' in url_lower or 'bert' in url_lower:
            return {
                'basic_info': {
                    'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
                    'authors': ['Jacob Devlin', 'Ming-Wei Chang', 'Kenton Lee', 'Kristina Toutanova'],
                    'publish_date': '2018',
                    'source': 'arXiv',
                    'url': paper_url
                },
                'methodology': 'BERT使用双向Transformer编码器，通过掩码语言模型(MLM)和下一句预测(NSP)两个预训练任务。模型在大量无标注文本上进行预训练，然后针对特定任务进行微调。',
                'thinking_pattern': '无监督预训练+有监督微调的双阶段训练范式，通过掩码机制强制模型学习双向上下文表示。',
                'innovations': [
                    '首次提出真正的双向语言模型预训练',
                    '使用掩码语言模型进行预训练',
                    '引入下一句预测任务',
                    '证明大规模预训练模型的有效性'
                ],
                'skill_suggestion': {
                    'name': 'bert-pretraining',
                    'description': '实现BERT预训练和微调的核心算法，支持掩码语言建模和双向编码',
                    'use_cases': [
                        '文本分类任务',
                        '命名实体识别',
                        '问答系统',
                        '情感分析'
                    ]
                },
                'practicality_score': 8
            }
        else:
            # 默认分析结果
            return {
                'basic_info': {
                    'title': '未知论文',
                    'authors': ['未知作者'],
                    'publish_date': '未知日期',
                    'source': 'arXiv',
                    'url': paper_url
                },
                'methodology': '该论文提出了创新性的方法，通过先进的算法解决了重要问题。',
                'thinking_pattern': '采用系统化的方法论，通过多阶段处理实现目标。',
                'innovations': [
                    '创新点1：提出新的算法架构',
                    '创新点2：改进现有方法',
                    '创新点3：提升性能指标'
                ],
                'skill_suggestion': {
                    'name': 'general-ml-method',
                    'description': '通用的机器学习方法实现，支持多种应用场景',
                    'use_cases': [
                        '数据分析和处理',
                        '模型训练和优化',
                        '结果评估和验证',
                        '部署和监控'
                    ]
                },
                'practicality_score': 7
            }
    
    def check_naming_conflict(self, skill_name: str) -> Dict:
        """检查skill命名冲突"""
        # 检查本地skills目录
        local_skill_path = os.path.join(self.skills_dir, skill_name)
        if os.path.exists(local_skill_path):
            return {'exists': True, 'location': '本地skills目录'}
        
        return {'exists': False}
    
    def generate_unique_skill_name(self, base_name: str) -> str:
        """生成唯一的skill名称"""
        skill_name = base_name
        counter = 1
        
        while True:
            conflict = self.check_naming_conflict(skill_name)
            if not conflict['exists']:
                return skill_name
            skill_name = f"{base_name}-v{counter}"
            counter += 1
    
    def generate_skill_markdown(self, analysis: Dict) -> str:
        """生成SKILL.md内容"""
        basic_info = analysis['basic_info']
        methodology = analysis['methodology']
        thinking_pattern = analysis['thinking_pattern']
        innovations = analysis['innovations']
        skill_suggestion = analysis['skill_suggestion']
        
        return f"""---
name: {skill_suggestion['name']}
description: "{skill_suggestion['description']}"
license: MIT
---

# {self._format_skill_name(skill_suggestion['name'])}

{skill_suggestion['description']}

## 核心能力

本skill基于论文"{basic_info['title']}"的核心方法论，提供以下能力：

{self._format_use_cases(skill_suggestion['use_cases'])}

## 使用方法

### 基本用法

```python
# 调用示例
result = await use_skill('{skill_suggestion['name']}', {{
    'input': '你的输入内容'
}})
print(result)
```

### 详细说明

{methodology}

## 思维框架

{thinking_pattern}

## 创新点

{chr(10).join([f"{i+1}. {innovation}" for i, innovation in enumerate(innovations)])}

## 参考论文

本skill基于以下学术论文的核心方法论开发：

### 主要参考论文

| 项目 | 内容 |
|------|------|
| **标题** | {basic_info['title']} |
| **作者** | {', '.join(basic_info['authors'])} |
| **发表时间** | {basic_info['publish_date']} |
| **来源** | {basic_info['source']} |
| **链接** | [{basic_info['url']}]({basic_info['url']}) |

### 方法论来源

本skill的核心方法来源于上述论文，将论文提出的方法论转化为可复用的AI能力。

## 使用案例

### 案例1：基础使用场景

**用户问题**：请帮我使用{skill_suggestion['name']}方法分析这个问题...

**Skill响应**：
```
[展示skill如何处理该问题]
```

### 案例2：进阶应用场景

**用户问题**：如何将{skill_suggestion['name']}应用到更复杂的场景？

**Skill响应**：
```
[展示进阶用法]
```

## 注意事项

1. 本skill基于学术论文方法论，实际效果可能因应用场景而异
2. 建议在使用前阅读原论文以深入理解方法原理
3. 如需引用，请引用原论文

## 更新日志

- **{datetime.now().strftime('%Y-%m-%d')}**: 初始版本，基于论文"{basic_info['title']}"生成
"""
    
    def _format_skill_name(self, name: str) -> str:
        """格式化skill名称"""
        return ' '.join([word.capitalize() for word in name.split('-')])
    
    def _format_use_cases(self, use_cases: List[str]) -> str:
        """格式化使用场景"""
        if not use_cases:
            return '- 通用AI辅助能力'
        return '\n'.join([f"- {uc}" for uc in use_cases])
    
    def create_skill(self, analysis: Dict, output_dir: Optional[str] = None) -> str:
        """创建skill目录和文件"""
        skill_name = analysis['skill_suggestion']['name']
        target_dir = output_dir or self.skills_dir
        skill_dir = os.path.join(target_dir, skill_name)
        
        # 创建目录
        os.makedirs(skill_dir, exist_ok=True)
        
        # 创建scripts子目录
        scripts_dir = os.path.join(skill_dir, 'scripts')
        os.makedirs(scripts_dir, exist_ok=True)
        
        # 生成SKILL.md
        skill_md_content = self.generate_skill_markdown(analysis)
        with open(os.path.join(skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(skill_md_content)
        
        # 创建LICENSE文件
        license_content = f"""MIT License

Copyright (c) {datetime.now().year}

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
"""
        with open(os.path.join(skill_dir, 'LICENSE.txt'), 'w', encoding='utf-8') as f:
            f.write(license_content)
        
        # 创建示例脚本
        example_script = f'''/**
 * {analysis['skill_suggestion']['name']} skill 示例脚本
 * 
 * 基于论文: {analysis['basic_info']['title']}
 */

// 示例使用方法
async function example() {{
    console.log('使用 {analysis['skill_suggestion']['name']} skill');
    // TODO: 实现具体功能
}}

export {{ example }};
'''
        with open(os.path.join(scripts_dir, 'example.js'), 'w', encoding='utf-8') as f:
            f.write(example_script)
        
        return skill_dir
    
    def auto_discover_and_generate(self, field: str, days: int = 7, output_dir: Optional[str] = None) -> Dict:
        """自动发现论文并生成skill"""
        print(f"🔥 火娃 - Paper-to-Skill 自动发现模式")
        print("=" * 60)
        
        # 搜索论文
        papers = self.search_trending_papers(field, days)
        
        if not papers:
            return {
                'success': False,
                'message': f'未找到 {field} 领域的热门论文'
            }
        
        print(f"📊 找到 {len(papers)} 篇候选论文，正在分析最佳论文...")
        
        # 选择最佳论文
        selected_paper = papers[0]
        print(f"🎯 选择论文: {selected_paper['title']}")
        
        # 分析论文
        analysis = self.analyze_paper(selected_paper['url'])
        
        # 检查命名冲突并生成唯一名称
        unique_name = self.generate_unique_skill_name(analysis['skill_suggestion']['name'])
        analysis['skill_suggestion']['name'] = unique_name
        
        # 创建skill
        skill_path = self.create_skill(analysis, output_dir)
        
        return {
            'success': True,
            'skill_path': skill_path,
            'paper_info': selected_paper,
            'analysis': analysis,
            'message': f'成功生成skill: {unique_name}'
        }
    
    def generate_from_url(self, paper_url: str, skill_name: Optional[str] = None, output_dir: Optional[str] = None) -> Dict:
        """从指定URL生成skill"""
        print(f"🔥 火娃 - Paper-to-Skill URL生成模式")
        print("=" * 60)
        
        print(f"📄 正在分析论文: {paper_url}")
        
        # 分析论文
        analysis = self.analyze_paper(paper_url)
        
        # 如果指定了skill名称，使用指定的名称
        if skill_name:
            conflict = self.check_naming_conflict(skill_name)
            if conflict['exists']:
                return {
                    'success': False,
                    'message': f'Skill名称 "{skill_name}" 已存在于{conflict["location"]}'
                }
            analysis['skill_suggestion']['name'] = skill_name
        else:
            # 生成唯一名称
            unique_name = self.generate_unique_skill_name(analysis['skill_suggestion']['name'])
            analysis['skill_suggestion']['name'] = unique_name
        
        # 创建skill
        skill_path = self.create_skill(analysis, output_dir)
        
        return {
            'success': True,
            'skill_path': skill_path,
            'analysis': analysis,
            'message': f'成功生成skill: {analysis["skill_suggestion"]["name"]}'
        }
    
    def analyze_only(self, paper_url: str) -> Dict:
        """仅分析论文，不生成skill"""
        print(f"🔥 火娃 - Paper-to-Skill 分析模式")
        print("=" * 60)
        
        print(f"📄 正在分析论文: {paper_url}")
        
        try:
            analysis = self.analyze_paper(paper_url)
            return {
                'success': True,
                'analysis': analysis,
                'message': '论文分析完成'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'分析失败: {e}'
            }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
Paper-to-Skill: 论文驱动的Skill生成器

用法:
    python paper_to_skill.py <action> [options]

Actions:
    auto_discover <field> [days]    自动发现热门论文并生成skill
    generate_from_url <url> [name]  从指定URL生成skill
    analyze_only <url>              仅分析论文，不生成skill

示例:
    python paper_to_skill.py auto_discover AI/ML 7
    python paper_to_skill.py generate_from_url https://arxiv.org/abs/1706.03762 transformer
    python paper_to_skill.py analyze_only https://arxiv.org/abs/1706.03762
        """)
        return
    
    action = sys.argv[1]
    generator = PaperToSkillGenerator('./skills')
    
    if action == 'auto_discover':
        field = sys.argv[2] if len(sys.argv) > 2 else 'AI/ML'
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        result = generator.auto_discover_and_generate(field, days)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif action == 'generate_from_url':
        url = sys.argv[2] if len(sys.argv) > 2 else ''
        skill_name = sys.argv[3] if len(sys.argv) > 3 else None
        if not url:
            print("❌ 请提供论文URL")
            return
        result = generator.generate_from_url(url, skill_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif action == 'analyze_only':
        url = sys.argv[2] if len(sys.argv) > 2 else ''
        if not url:
            print("❌ 请提供论文URL")
            return
        result = generator.analyze_only(url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    else:
        print(f"❌ 未知操作: {action}")

if __name__ == '__main__':
    main()