---
name: web-search
description: "升级版Web搜索和内容提取技能，提供多搜索引擎支持、智能排序、质量评估、高级搜索和缓存功能"
homepage: https://duckduckgo.com
metadata: {"nanobot":{"emoji":"🔍🚀"}}
---

# Web Search Upgraded

升级版的Web搜索和内容提取技能，提供更高质量的搜索结果和更丰富的功能。

## 🎯 主要特性

### 🔍 多搜索引擎支持
- **Brave Search**: 高质量搜索（需要API key）
- **DuckDuckGo**: 免费搜索（无需API key）
- **Bing**: 微软搜索（需要API key）
- **智能引擎切换**: 按优先级自动切换，提高成功率

### 🎯 高级搜索功能
- **时间范围过滤**: 1h/24h/7d/30d
- **来源过滤**: news/academic/web
- **语言过滤**: zh/en
- **地区过滤**: cn/us/uk/etc

### 📊 智能结果排序和评分
- **相关性评分**: 0-10分，基于关键词匹配
- **质量评分**: 0-10分，基于URL结构和内容质量
- **综合评分**: 相关性70% + 质量30%
- **智能排序**: 最相关的结果排在前面

### 📈 内容质量评估
- **URL质量评估**: 长度、结构、可信度
- **标题质量评估**: 长度、关键词匹配
- **摘要质量评估**: 长度、信息密度
- **来源可信度**: 优先显示.gov/.edu/.org等可信来源

### 💾 搜索历史和缓存
- **智能缓存**: 基于查询和过滤条件缓存结果
- **缓存有效期**: 默认1小时
- **搜索历史**: 保存最近100次搜索
- **缓存管理**: 支持清除缓存和搜索历史

### 🔄 结果去重功能
- **URL去重**: 基于MD5哈希去重
- **智能合并**: 相同URL的结果合并
- **避免重复**: 确保结果唯一性

### 📄 改进的URL抓取和内容提取
- **多格式支持**: text/markdown
- **HTML清理**: 移除script/style标签
- **内容提取**: 智能提取正文内容
- **错误处理**: 更好的异常处理和重试机制

## 🚀 使用方法

### 基本搜索

```python
from web_search import WebSearch

# 创建搜索实例
ws = WebSearch()

# 基本搜索
results = ws.search("A股股票列表", max_results=10)

# 查看结果
for result in results:
    print(f"{result['title']}")
    print(f"  URL: {result['url']}")
    print(f"  来源: {result['source']}")
    print(f"  相关度: {result['score']:.2f}")
    print(f"  质量分: {result['quality_score']:.2f}")
    print(f"  摘要: {result['snippet'][:100]}...")
    print()
```

### 高级搜索

```python
# 时间范围搜索
results = ws.search(
    query="人工智能发展趋势",
    max_results=5,
    time_range="7d"  # 最近7天
)

# 语言和地区过滤
results = ws.search(
    query="Python编程教程",
    max_results=5,
    language="en",  # 英文
    region="us"     # 美国
)

# 来源过滤
results = ws.search(
    query="学术论文",
    max_results=5,
    source="academic"  # 学术来源
)
```

### URL内容抓取

```python
# 抓取文本内容
content = ws.fetch_url("https://www.python.org", extract_mode="text")

# 抓取Markdown格式
markdown = ws.fetch_url("https://www.python.org", extract_mode="markdown")
```

### 文本摘要

```python
# 生成摘要
summary = ws.summarize(content, max_sentences=3)
print(f"摘要: {summary}")
```

### 结果导出

```python
# 导出CSV
results = ws.search("Python编程教程", max_results=5)
ws.export_results(results, format="csv", filename="search_results.csv")

# 导出JSON
ws.export_results(results, format="json", filename="search_results.json")
```

### 搜索历史

```python
# 获取搜索历史
history = ws.get_search_history(limit=10)

for item in history:
    print(f"查询: '{item['query']}' - 结果数: {item['results_count']}")
```

### 缓存管理

```python
# 搜索（会缓存结果）
results = ws.search("Python编程教程", max_results=3)

# 再次搜索（会使用缓存）
results = ws.search("Python编程教程", max_results=3)

# 清除缓存
ws.clear_cache()

# 清除搜索历史
ws.clear_history()
```

## 📊 搜索结果格式

```python
{
    'title': '搜索结果标题',
    'url': 'https://example.com',
    'snippet': '搜索结果摘要...',
    'source': 'duckduckgo',  # brave/duckduckgo/bing
    'score': 8.50,  # 相关度评分 (0-10)
    'quality_score': 7.20,  # 质量评分 (0-10)
    'timestamp': '2026-03-11T16:14:00'
}
```

## 🔧 配置

### API Key配置

Brave Search和Bing需要API key才能使用：

```python
from web_search import WebSearch

ws = WebSearch()

# 配置Brave Search API key
ws.search_engine.engines['brave']['api_key'] = 'your-brave-api-key'

# 配置Bing API key
ws.search_engine.engines['bing']['api_key'] = 'your-bing-api-key'
```

### 缓存配置

```python
from web_search import WebSearch

# 自定义缓存目录
ws = WebSearch(cache_dir='/path/to/cache')

# 自定义缓存有效期（小时）
ws = WebSearch(cache_dir='/path/to/cache', history_limit=50)
```

## 🎨 使用示例

### 示例1: 股票市场研究

```python
from web_search import WebSearch

ws = WebSearch()

# 搜索A股相关信息
results = ws.search("A股市场分析 2024", max_results=5)

print("A股市场分析结果:")
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
    print(f"   相关度: {result['score']:.2f}")
    print(f"   质量分: {result['quality_score']:.2f}")
    print(f"   摘要: {result['snippet'][:150]}...")
    print()

# 抓取相关网页内容
for result in results[:2]:
    url = result['url']
    content = ws.fetch_url(url, extract_mode="text")
    print(f"\n抓取内容 ({len(content)} 字符):")
    print(content[:500])
```

### 示例2: 学术论文搜索

```python
from web_search import WebSearch

ws = WebSearch()

# 搜索学术论文
results = ws.search(
    query="机器学习算法研究",
    max_results=10,
    language="zh",
    source="academic"
)

# 筛选arXiv论文
papers = [r for r in results if 'arxiv.org' in r['url']]

print(f"找到 {len(papers)} 篇arXiv论文:")
for i, paper in enumerate(papers, 1):
    print(f"{i}. {paper['title']}")
    print(f"   URL: {paper['url']}")
    print(f"   相关度: {paper['score']:.2f}")
    print()

# 导出结果
ws.export_results(papers, format="json", filename="papers.json")
```

### 示例3: 新闻监控

```python
from web_search import WebSearch

ws = WebSearch()

# 搜索最新新闻
results = ws.search(
    query="科技新闻 最新",
    max_results=5,
    time_range="24h",  # 最近24小时
    region="cn"
)

print("最新科技新闻:")
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
    print(f"   来源: {result['source']}")
    print(f"   相关度: {result['score']:.2f}")
    print(f"   摘要: {result['snippet'][:150]}...")
    print()

# 抓取新闻内容
for result in results:
    url = result['url']
    content = ws.fetch_url(url, extract_mode="text")
    print(f"\n新闻内容 ({len(content)} 字符):")
    print(content[:500])
```

## 📈 性能优化

### 1. 使用缓存

```python
# 搜索（会缓存结果）
results = ws.search("Python编程教程", max_results=3)

# 再次搜索（会使用缓存，速度更快）
results = ws.search("Python编程教程", max_results=3)
```

### 2. 限制结果数量

```python
# 只搜索前5个结果
results = ws.search("Python编程教程", max_results=5)
```

### 3. 使用语言和地区过滤

```python
# 只搜索中文结果
results = ws.search("Python编程教程", max_results=10, language="zh", region="cn")
```

## ⚠️ 注意事项

### 1. API Key配置
- Brave Search和Bing需要API key才能使用
- DuckDuckGo免费使用，无需API key
- API key可以配置在代码中或环境变量中

### 2. 搜索频率
- 避免过于频繁的搜索请求
- 使用缓存减少重复搜索
- 合理设置max_results参数

### 3. 缓存管理
- 缓存默认有效期1小时
- 可以手动清除缓存
- 缓存文件存储在~/.nanobot/cache/web_search/

### 4. 错误处理
- 网络请求可能失败
- 某些搜索引擎可能不可用
- 建议添加错误处理和重试机制

## 🎯 最佳实践

### 1. 搜索技巧
- 使用具体的关键词获得更好的结果
- 结合多个关键词进行搜索
- 限制结果数量以提高效率
- 使用语言和地区过滤提高相关性

### 2. 结果分析
- 关注相关度评分
- 查看质量评分
- 分析来源分布
- 检查URL质量

### 3. 缓存使用
- 重复搜索使用缓存
- 定期清除缓存
- 监控缓存大小
- 合理设置缓存有效期

### 4. 错误处理
- 添加异常捕获
- 实现重试机制
- 提供备用搜索引擎
- 记录错误日志

## 📚 更多文档

- **UPGRADE_REPORT.md**: 升级报告，详细说明升级内容
- **usage_examples.md**: 使用示例和最佳实践
- **test_search_upgraded.py**: 测试脚本
- **demo_upgraded.py**: 功能演示脚本

## 🎉 总结

升级版web-search技能提供了：

1. ✅ **更高质量的搜索结果**: 多引擎并行搜索，智能排序
2. ✅ **更丰富的搜索功能**: 时间、来源、语言过滤
3. ✅ **更智能的评分系统**: 相关度+质量评分
4. ✅ **更完善的缓存机制**: 智能缓存，减少重复搜索
5. ✅ **更便捷的搜索历史**: 方便回顾和重复搜索
6. ✅ **更好的用户体验**: 丰富的信息展示，友好的界面

---

**版本**: v2.0
**更新时间**: 2026-03-11
**作者**: 火娃 (nanobot)