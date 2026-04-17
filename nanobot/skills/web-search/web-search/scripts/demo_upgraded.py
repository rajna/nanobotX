#!/usr/bin/env python3
"""
升级版Web搜索演示脚本

展示升级版web-search技能的所有功能。
"""

import sys
import os

# 添加技能路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_search import WebSearch

def demo_basic_search():
    """演示基本搜索功能"""
    print("🔍 演示基本搜索功能")
    print("=" * 60)

    ws = WebSearch()

    # 基本搜索
    print("\n1. 基本搜索:")
    results = ws.search("A股股票列表", max_results=5)

    print(f"   找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result.get('title', '无标题')}")
        print(f"      URL: {result.get('url', '无链接')}")
        print(f"      来源: {result.get('source', 'unknown')}")
        print(f"      相关度: {result.get('score', 0):.2f}")
        print(f"      质量分: {result.get('quality_score', 0):.2f}")
        print(f"      摘要: {result.get('snippet', '无摘要')[:100]}...")
        print()

def demo_advanced_search():
    """演示高级搜索功能"""
    print("🎯 演示高级搜索功能")
    print("=" * 60)

    ws = WebSearch()

    # 时间范围搜索
    print("\n1. 时间范围搜索（最近7天）:")
    results = ws.search("人工智能发展趋势", max_results=5, time_range="7d")

    print(f"   找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result.get('title', '无标题')}")
        print(f"      相关度: {result.get('score', 0):.2f}")
        print(f"      质量分: {result.get('quality_score', 0):.2f}")
        print()

    # 语言和地区过滤
    print("\n2. 语言和地区过滤:")
    results = ws.search("Python编程教程", max_results=5, language="en", region="us")

    print(f"   找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result.get('title', '无标题')}")
        print(f"      相关度: {result.get('score', 0):.2f}")
        print(f"      质量分: {result.get('quality_score', 0):.2f}")
        print()

def demo_url_fetching():
    """演示URL抓取功能"""
    print("📄 演示URL内容抓取功能")
    print("=" * 60)

    ws = WebSearch()

    # 抓取网页内容
    print("\n1. 抓取网页内容:")
    url = "https://www.python.org"
    content = ws.fetch_url(url, extract_mode="text")

    print(f"   抓取成功！内容长度: {len(content)} 字符")
    print(f"   前200字符: {content[:200]}...")

    # 抓取markdown格式
    print("\n2. 抓取Markdown格式:")
    markdown_content = ws.fetch_url(url, extract_mode="markdown")

    print(f"   抓取成功！内容长度: {len(markdown_content)} 字符")
    print(f"   前200字符: {markdown_content[:200]}...")

def demo_text_summarization():
    """演示文本摘要功能"""
    print("📝 演示文本摘要功能")
    print("=" * 60)

    ws = WebSearch()

    # 抓取内容
    url = "https://www.python.org"
    content = ws.fetch_url(url, extract_mode="text")

    # 生成摘要
    print("\n1. 生成文本摘要:")
    summary = ws.summarize(content, max_sentences=3)

    print(f"   摘要内容:")
    print(f"   {summary}")

def demo_export():
    """演示结果导出功能"""
    print("💾 演示结果导出功能")
    print("=" * 60)

    ws = WebSearch()

    # 搜索并导出
    print("\n1. 搜索并导出CSV:")
    results = ws.search("Python编程教程", max_results=5)
    success = ws.export_results(results, format="csv", filename="demo_results_upgraded.csv")

    if success:
        print(f"   ✅ 结果已导出到: demo_results_upgraded.csv")

    # 搜索并导出JSON
    print("\n2. 搜索并导出JSON:")
    results = ws.search("人工智能发展趋势", max_results=5)
    success = ws.export_results(results, format="json", filename="demo_results_upgraded.json")

    if success:
        print(f"   ✅ 结果已导出到: demo_results_upgraded.json")

def demo_search_history():
    """演示搜索历史功能"""
    print("📜 演示搜索历史功能")
    print("=" * 60)

    ws = WebSearch()

    # 搜索几次
    print("\n1. 执行几次搜索:")
    ws.search("A股股票列表", max_results=3)
    ws.search("Python编程教程", max_results=3)
    ws.search("人工智能发展趋势", max_results=3)

    # 获取历史
    print("\n2. 获取搜索历史:")
    history = ws.get_search_history(limit=5)

    print(f"   搜索历史 ({len(history)} 条):")
    for i, item in enumerate(history, 1):
        print(f"   {i}. 查询: '{item.get('query', '')}' - 结果数: {item.get('results_count', 0)}")

def demo_cache_management():
    """演示缓存管理功能"""
    print("🔧 演示缓存管理功能")
    print("=" * 60)

    ws = WebSearch()

    # 搜索（会缓存）
    print("\n1. 执行搜索（会缓存结果）:")
    results = ws.search("Python编程教程", max_results=3)
    print(f"   找到 {len(results)} 个结果")

    # 再次搜索（会使用缓存）
    print("\n2. 再次搜索（会使用缓存）:")
    results = ws.search("Python编程教程", max_results=3)
    print(f"   找到 {len(results)} 个结果")

    # 清除缓存
    print("\n3. 清除缓存:")
    ws.clear_cache()
    print(f"   ✅ 缓存已清除")

def demo_comparison():
    """演示新旧版本对比"""
    print("🆚 升级版 vs 原版对比")
    print("=" * 60)

    print("\n升级版新增功能:")
    print("  ✅ 多搜索引擎支持（Brave、DuckDuckGo、Bing）")
    print("  ✅ 高级搜索功能（时间、来源、语言过滤）")
    print("  ✅ 智能结果排序和评分")
    print("  ✅ 内容质量评估")
    print("  ✅ 搜索历史和缓存")
    print("  ✅ 结果去重功能")
    print("  ✅ 改进的URL抓取和内容提取")
    print("  ✅ 更好的错误处理")

    print("\n搜索结果质量提升:")
    print("  📊 相关性评分：0-10分")
    print("  📊 质量评分：0-10分")
    print("  📊 综合评分：相关性70% + 质量30%")
    print("  📊 智能排序：最相关的结果排在前面")

    print("\n性能优化:")
    print("  ⚡ 搜索缓存：减少重复搜索时间")
    print("  ⚡ 智能去重：避免重复结果")
    print("  ⚡ 多引擎并行：提高搜索成功率")

def main():
    """主演示函数"""
    print("🚀 升级版Web搜索技能演示")
    print("=" * 60)
    print("这是一个升级版的web-search技能，提供了更高质量的搜索结果！")
    print()

    demos = [
        ("基本搜索", demo_basic_search),
        ("高级搜索", demo_advanced_search),
        ("URL抓取", demo_url_fetching),
        ("文本摘要", demo_text_summarization),
        ("结果导出", demo_export),
        ("搜索历史", demo_search_history),
        ("缓存管理", demo_cache_management),
        ("版本对比", demo_comparison)
    ]

    for demo_name, demo_func in demos:
        try:
            demo_func()
            print(f"\n✅ {demo_name} 演示完成")
            print("-" * 60)
        except Exception as e:
            print(f"\n❌ {demo_name} 演示失败: {e}")
            import traceback
            traceback.print_exc()
            print("-" * 60)

    print("\n🎉 所有演示完成！")
    print("升级版web-search技能提供了更高质量的搜索结果！")

if __name__ == "__main__":
    main()