---
name: web-search
description: Web search and content extraction with support for multiple search engines and content analysis. Use when the user needs to search the web, extract content from URLs, or perform research tasks.
---

# Web Search

Comprehensive web search and content extraction skill for research and information gathering.

## Features

- 🔍 Web search with multiple search engines
- 📄 Content extraction from URLs
- 📝 Text summarization and analysis
- 💾 Search result export
- 🔗 URL fetching and parsing

## Usage

### Web Search

```python
import web_search as ws

# Basic search
results = ws.search("A股股票列表", max_results=10)

# Advanced search with filters
results = ws.search(
    query="人工智能发展趋势",
    max_results=5,
    language="zh",
    region="cn"
)
```

### URL Content Extraction

```python
# Extract content from URL
content = ws.fetch_url("https://example.com")
summary = ws.summarize(content)

# Extract specific content type
text_content = ws.fetch_url("https://example.com", extract_mode="text")
markdown_content = ws.fetch_url("https://example.com", extract_mode="markdown")
```

### Search and Export

```python
# Search and export results
results = ws.search("Python编程教程", max_results=5)
ws.export_results(results, format="csv", filename="search_results.csv")
```

## Search Engines

- **Brave Search**: Requires API key for advanced features
- **DuckDuckGo**: Free, no API key required
- **Bing**: Requires API key for commercial use
- **Google**: Requires API key

## Configuration

Create a configuration file at `~/.nanobot/config.json`:

```json
{
  "tools": {
    "web": {
      "search": {
        "apiKey": "your-api-key",
        "maxResults": 5,
        "engine": "brave"
      }
    }
  }
}
```

## Examples

### Example 1: Stock Market Research
```python
# Search for stock market information
results = ws.search("A股市场分析 2024", max_results=5)
for result in results:
    print(f"{result['title']}: {result['url']}")
```

### Example 2: Academic Research
```python
# Search for academic papers
results = ws.search("机器学习算法研究", max_results=10, language="zh")
papers = [r for r in results if 'arxiv.org' in r['url'] or 'scholar.google' in r['url']]
```

### Example 3: News Monitoring
```python
# Search for recent news
results = ws.search("科技新闻 最新", max_results=5, region="cn")
news = ws.extract_news_content(results)
```

## Error Handling

- Handle API rate limits
- Fallback to free search engines
- Network timeout handling
- Content extraction errors

## Performance Tips

- Use specific queries for better results
- Limit results to what you need
- Use language filters for relevant content
- Cache results for repeated queries