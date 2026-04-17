#!/usr/bin/env python3
"""
Web搜索和内容提取模块（简化接口）

这是升级版web-search的简化接口，提供用户友好的API。
"""

import sys
import os
from typing import List, Dict

# 添加升级版web_search到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_search_upgraded import WebSearchUpgraded

class WebSearch:
    """Web搜索类（简化接口）"""

    def __init__(self):
        self.search_engine = WebSearchUpgraded()

    def search(
        self,
        query: str,
        max_results: int = 10,
        language: str = "zh",
        region: str = "cn",
        time_range: str = None,
        source: str = None,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        执行web搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数
            language: 语言 (zh/en)
            region: 地区 (cn/us/uk/etc)
            time_range: 时间范围 (1h/24h/7d/30d)
            source: 来源过滤 (news/academic/web)
            use_cache: 是否使用缓存

        Returns:
            搜索结果列表
        """
        return self.search_engine.search(
            query=query,
            max_results=max_results,
            language=language,
            region=region,
            time_range=time_range,
            source=source,
            use_cache=use_cache
        )

    def fetch_url(
        self,
        url: str,
        extract_mode: str = "markdown",
        max_chars: int = 10000
    ) -> str:
        """
        抓取URL内容

        Args:
            url: URL地址
            extract_mode: 提取模式 (text/markdown)
            max_chars: 最大字符数

        Returns:
            抓取的内容
        """
        return self.search_engine.fetch_url(
            url=url,
            extract_mode=extract_mode,
            max_chars=max_chars
        )

    def summarize(self, text: str, max_sentences: int = 3) -> str:
        """
        文本摘要

        Args:
            text: 输入文本
            max_sentences: 最大句子数

        Returns:
            摘要文本
        """
        return self.search_engine.summarize(text, max_sentences)

    def export_results(
        self,
        results: List[Dict],
        format: str = "csv",
        filename: str = "search_results.csv"
    ) -> bool:
        """
        导出搜索结果

        Args:
            results: 搜索结果列表
            format: 导出格式 (csv/json)
            filename: 文件名

        Returns:
            是否成功
        """
        return self.search_engine.export_results(results, format, filename)

    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """获取搜索历史"""
        return self.search_engine.get_search_history(limit)

    def clear_cache(self):
        """清除缓存"""
        self.search_engine.clear_cache()

    def clear_history(self):
        """清除搜索历史"""
        self.search_engine.clear_history()

# 创建全局实例
web_search = WebSearch()

# 如果直接运行此脚本，进行测试
if __name__ == "__main__":
    print("🔥 火娃 - Web搜索模块测试")
    print("=" * 60)

    # 测试搜索功能
    print("\n🔍 测试搜索功能...")
    results = web_search.search("A股股票列表", max_results=5)

    print(f"\n搜索结果 ({len(results)} 个):")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('title', '无标题')}")
        print(f"   URL: {result.get('url', '无链接')}")
        print(f"   来源: {result.get('source', 'unknown')}")
        print(f"   相关度: {result.get('score', 0):.2f}")
        print(f"   质量分: {result.get('quality_score', 0):.2f}")
        print(f"   摘要: {result.get('snippet', '无摘要')[:150]}...")
        print()

    # 测试URL抓取
    print("\n📄 测试URL抓取...")
    url = "https://www.python.org"
    content = web_search.fetch_url(url, extract_mode="text")
    print(f"抓取内容长度: {len(content)} 字符")
    print(f"前200字符: {content[:200]}...")

    print("\n✅ 测试完成！")