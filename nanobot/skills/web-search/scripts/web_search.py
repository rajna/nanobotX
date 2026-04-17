#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Search Skill - Python实现
支持多搜索引擎搜索和URL内容提取
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime


class WebSearch:
    """Web搜索类"""

    def __init__(self, max_results: int = 10, timeout: int = 10):
        """
        初始化Web搜索

        Args:
            max_results: 最大结果数
            timeout: 请求超时时间（秒）
        """
        self.max_results = max_results
        self.timeout = timeout
        self.search_history = []

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        language: str = "zh",
        region: str = "cn",
        engine: str = "duckduckgo"
    ) -> List[Dict[str, Any]]:
        """
        执行网络搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数（覆盖默认值）
            language: 语言（zh/en）
            region: 地区（cn/us等）
            engine: 搜索引擎（duckduckgo/brave/bing）

        Returns:
            搜索结果列表，每个结果包含title、url、snippet
        """
        max_results = max_results or self.max_results

        if engine == "duckduckgo":
            return self._search_duckduckgo(query, max_results, language, region)
        elif engine == "brave":
            return self._search_brave(query, max_results, language, region)
        elif engine == "bing":
            return self._search_bing(query, max_results, language, region)
        else:
            print(f"警告: 不支持的搜索引擎 '{engine}'，使用DuckDuckGo")
            return self._search_duckduckgo(query, max_results, language, region)

    def _search_duckduckgo(
        self,
        query: str,
        max_results: int,
        language: str,
        region: str
    ) -> List[Dict[str, Any]]:
        """
        使用DuckDuckGo搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数
            language: 语言
            region: 地区

        Returns:
            搜索结果列表
        """
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1,
                "max_results": max_results
            }

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            results = []
            if "AbstractText" in data:
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("AbstractText", ""),
                    "source": "duckduckgo"
                })

            if "RelatedTopics" in data:
                for topic in data["RelatedTopics"][:max_results - len(results)]:
                    if isinstance(topic, dict):
                        result = topic.get("Text", "")
                        url = topic.get("FirstURL", "")

                        if result and url:
                            # 提取标题（去掉" - "后面的内容）
                            title = result.split(" - ")[0] if " - " in result else result[:50]
                            results.append({
                                "title": title,
                                "url": url,
                                "snippet": result,
                                "source": "duckduckgo"
                            })

            return results[:max_results]

        except Exception as e:
            print(f"DuckDuckGo搜索失败: {e}")
            return []

    def _search_brave(
        self,
        query: str,
        max_results: int,
        language: str,
        region: str
    ) -> List[Dict[str, Any]]:
        """
        使用Brave Search（需要API key）

        Args:
            query: 搜索查询
            max_results: 最大结果数
            language: 语言
            region: 地区

        Returns:
            搜索结果列表
        """
        try:
            # 检查API key
            api_key = self._get_brave_api_key()
            if not api_key:
                print("警告: Brave Search需要API key，使用DuckDuckGo")
                return self._search_duckduckgo(query, max_results, language, region)

            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key
            }
            params = {
                "q": query,
                "count": max_results,
                "text_decorations": False,
                "search_lang": language,
                "region": region
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "source": "brave"
                })

            return results

        except Exception as e:
            print(f"Brave Search搜索失败: {e}")
            return []

    def _search_bing(
        self,
        query: str,
        max_results: int,
        language: str,
        region: str
    ) -> List[Dict[str, Any]]:
        """
        使用Bing搜索（需要API key）

        Args:
            query: 搜索查询
            max_results: 最大结果数
            language: 语言
            region: 地区

        Returns:
            搜索结果列表
        """
        try:
            # 检查API key
            api_key = self._get_bing_api_key()
            if not api_key:
                print("警告: Bing Search需要API key，使用DuckDuckGo")
                return self._search_duckduckgo(query, max_results, language, region)

            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key
            }
            params = {
                "q": query,
                "count": max_results,
                "mkt": f"{region}-{language.upper()}"
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            results = []
            for item in data.get("webPages", {}).get("value", []):
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "bing"
                })

            return results

        except Exception as e:
            print(f"Bing Search搜索失败: {e}")
            return []

    def _get_brave_api_key(self) -> Optional[str]:
        """获取Brave API key"""
        try:
            import os
            config_path = os.path.expanduser("~/.nanobot/config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("tools", {}).get("web", {}).get("search", {}).get("brave", {}).get("apiKey")
        except Exception as e:
            print(f"读取Brave API key失败: {e}")
        return None

    def _get_bing_api_key(self) -> Optional[str]:
        """获取Bing API key"""
        try:
            import os
            config_path = os.path.expanduser("~/.nanobot/config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("tools", {}).get("web", {}).get("search", {}).get("bing", {}).get("apiKey")
        except Exception as e:
            print(f"读取Bing API key失败: {e}")
        return None

    def fetch_url(
        self,
        url: str,
        extract_mode: str = "markdown",
        max_chars: int = 10000
    ) -> str:
        """
        获取URL内容

        Args:
            url: URL地址
            extract_mode: 提取模式（text/markdown）
            max_chars: 最大字符数

        Returns:
            提取的内容
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            if extract_mode == "text":
                return response.text[:max_chars]
            elif extract_mode == "markdown":
                # 简单的HTML转Markdown
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                return text[:max_chars]
            else:
                print(f"警告: 不支持的提取模式 '{extract_mode}'，使用text模式")
                return response.text[:max_chars]

        except Exception as e:
            print(f"获取URL内容失败: {e}")
            return ""

    def summarize(self, text: str, max_length: int = 500) -> str:
        """
        总结文本

        Args:
            text: 原始文本
            max_length: 最大长度

        Returns:
            总结文本
        """
        if len(text) <= max_length:
            return text

        # 简单的总结策略：取前max_length个字符
        return text[:max_length] + "..."

    def export_results(
        self,
        results: List[Dict[str, Any]],
        format: str = "json",
        filename: Optional[str] = None
    ) -> bool:
        """
        导出搜索结果

        Args:
            results: 搜索结果列表
            format: 导出格式（json/csv）
            filename: 文件名（可选）

        Returns:
            导出成功返回True
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"search_results_{timestamp}.{format}"

            if format == "json":
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
            elif format == "csv":
                import csv
                with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['title', 'url', 'snippet', 'source'])
                    for result in results:
                        writer.writerow([
                            result.get('title', ''),
                            result.get('url', ''),
                            result.get('snippet', ''),
                            result.get('source', '')
                        ])
            else:
                print(f"警告: 不支持的导出格式 '{format}'")
                return False

            print(f"搜索结果已导出到: {filename}")
            return True

        except Exception as e:
            print(f"导出搜索结果失败: {e}")
            return False


def main():
    """主函数：演示Web搜索功能"""

    # 创建搜索实例
    web_search = WebSearch(max_results=10)

    # 示例1: 搜索A股股票
    print("=" * 60)
    print("搜索A股股票信息")
    print("=" * 60)
    results = web_search.search("A股股票列表", max_results=5)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   摘要: {result['snippet'][:100]}...")

    # 示例2: 搜索今日股市行情
    print("\n" + "=" * 60)
    print("搜索今日股市行情")
    print("=" * 60)
    results = web_search.search("今日A股行情 2026", max_results=5)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   摘要: {result['snippet'][:100]}...")

    # 示例3: 导出结果
    print("\n" + "=" * 60)
    print("导出搜索结果")
    print("=" * 60)
    web_search.export_results(results, format="json", filename="search_results.json")

    print("\n✅ Web搜索演示完成！")


if __name__ == "__main__":
    main()
