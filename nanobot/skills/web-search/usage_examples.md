# Web Search Upgraded 使用示例

## 🎯 快速开始

### 1. 基本搜索

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

### 2. 高级搜索

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

### 3. URL内容抓取

```python
# 抓取文本内容
content = ws.fetch_url("https://www.python.org", extract_mode="text")
print(f"抓取内容长度: {len(content)} 字符")

# 抓取Markdown格式
markdown = ws.fetch_url("https://www.python.org", extract_mode="markdown")
print(f"Markdown内容长度: {len(markdown)} 字符")
```

### 4. 文本摘要

```python
# 生成摘要
summary = ws.summarize(content, max_sentences=3)
print(f"摘要: {summary}")
```

### 5. 结果导出

```python
# 导出CSV
results = ws.search("Python编程教程", max_results=5)
ws.export_results(results, format="csv", filename="search_results.csv")

# 导出JSON
ws.export_results(results, format="json", filename="search_results.json")
```

### 6. 搜索历史

```python
# 执行几次搜索
ws.search("A股股票列表", max_results=3)
ws.search("Python编程教程", max_results=3)
ws.search("人工智能发展趋势", max_results=3)

# 获取搜索历史
history = ws.get_search_history(limit=5)

for item in history:
    print(f"查询: '{item['query']}' - 结果数: {item['results_count']}")
```

### 7. 缓存管理

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

## 📋 实际使用场景

### 场景1: 股票市场研究

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
for result in results[:2]:  # 只抓取前2个结果
    url = result['url']
    content = ws.fetch_url(url, extract_mode="text")
    print(f"\n抓取内容 ({len(content)} 字符):")
    print(content[:500])
```

### 场景2: 学术论文搜索

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

### 场景3: 新闻监控

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

### 场景4: 技术文档搜索

```python
from web_search import WebSearch

ws = WebSearch()

# 搜索技术文档
results = ws.search(
    query="Python教程 官方文档",
    max_results=5,
    language="zh",
    region="cn"
)

print("技术文档搜索结果:")
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
    print(f"   URL: {result['url']}")
    print(f"   来源: {result['source']}")
    print(f"   相关度: {result['score']:.2f}")
    print(f"   质量分: {result['quality_score']:.2f}")
    print()

# 按质量排序
sorted_results = sorted(results, key=lambda x: x['quality_score'], reverse=True)

print("按质量排序的结果:")
for i, result in enumerate(sorted_results, 1):
    print(f"{i}. {result['title']}")
    print(f"   质量分: {result['quality_score']:.2f}")
    print()
```

### 场景5: 多语言搜索

```python
from web_search import WebSearch

ws = WebSearch()

# 中文搜索
results_zh = ws.search(
    query="人工智能发展",
    max_results=5,
    language="zh",
    region="cn"
)

# 英文搜索
results_en = ws.search(
    query="artificial intelligence development",
    max_results=5,
    language="en",
    region="us"
)

print("中文搜索结果:")
for result in results_zh:
    print(f"{result['title']} ({result['source']})")

print("\n英文搜索结果:")
for result in results_en:
    print(f"{result['title']} ({result['source']})")
```

## 🔧 高级用法

### 1. 批量搜索

```python
from web_search import WebSearch

ws = WebSearch()

# 批量搜索多个关键词
keywords = [
    "A股股票列表",
    "Python编程教程",
    "人工智能发展趋势"
]

all_results = []

for keyword in keywords:
    results = ws.search(keyword, max_results=3)
    all_results.extend(results)
    print(f"搜索 '{keyword}' 找到 {len(results)} 个结果")

# 去重
unique_results = ws.search_engine._deduplicate_results(all_results)

# 排序
sorted_results = ws.search_engine._sort_results(unique_results)

print(f"\n总共找到 {len(sorted_results)} 个唯一结果")
```

### 2. 自定义搜索

```python
from web_search import WebSearch

ws = WebSearch()

# 自定义搜索参数
results = ws.search(
    query="机器学习算法",
    max_results=10,
    language="zh",
    region="cn",
    time_range="30d",  # 最近30天
    source="web",
    use_cache=True  # 使用缓存
)

# 查看结果统计
print(f"总结果数: {len(results)}")

# 按来源统计
source_counts = {}
for result in results:
    source = result['source']
    source_counts[source] = source_counts.get(source, 0) + 1

print("\n来源统计:")
for source, count in source_counts.items():
    print(f"  {source}: {count} 个")

# 按质量统计
quality_scores = [result['quality_score'] for result in results]
avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

print(f"\n平均质量分: {avg_quality:.2f}")
```

### 3. 搜索结果分析

```python
from web_search import WebSearch

ws = WebSearch()

# 搜索
results = ws.search("Python编程教程", max_results=10)

# 分析结果
print("搜索结果分析:")
print("=" * 60)

# 1. 相关度分析
print("\n1. 相关度分析:")
scores = [r['score'] for r in results]
print(f"   最高相关度: {max(scores):.2f}")
print(f"   最低相关度: {min(scores):.2f}")
print(f"   平均相关度: {sum(scores)/len(scores):.2f}")

# 2. 质量分析
print("\n2. 质量分析:")
quality_scores = [r['quality_score'] for r in results]
print(f"   最高质量分: {max(quality_scores):.2f}")
print(f"   最低质量分: {min(quality_scores):.2f}")
print(f"   平均质量分: {sum(quality_scores)/len(quality_scores):.2f}")

# 3. 来源分析
print("\n3. 来源分析:")
source_counts = {}
for r in results:
    source = r['source']
    source_counts[source] = source_counts.get(source, 0) + 1

for source, count in source_counts.items():
    print(f"   {source}: {count} 个")

# 4. URL分析
print("\n4. URL分析:")
url_lengths = [len(r['url']) for r in results]
print(f"   最短URL: {min(url_lengths)} 字符")
print(f"   最长URL: {max(url_lengths)} 字符")
print(f"   平均URL长度: {sum(url_lengths)/len(url_lengths):.2f} 字符")
```

## 🎨 输出格式说明

### 搜索结果格式
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

### 搜索历史格式
```python
{
    'query': '搜索关键词',
    'results_count': 5,
    'timestamp': '2026-03-11T16:14:00'
}
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

## 📞 故障排除

### 1. 搜索无结果
- 检查网络连接
- 尝试不同的搜索引擎
- 调整搜索关键词
- 检查API key配置

### 2. URL抓取失败
- 检查URL是否有效
- 检查网络连接
- 检查目标网站是否可访问
- 调整超时设置

### 3. 缓存问题
- 清除缓存
- 检查缓存文件权限
- 检查磁盘空间
- 重新加载缓存

### 4. 性能问题
- 减少max_results参数
- 使用缓存减少重复搜索
- 限制搜索频率
- 优化查询关键词

---

**版本**: v2.0
**更新时间**: 2026-03-11
**作者**: 火娃 (nanobot)