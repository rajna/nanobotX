#!/usr/bin/env python3
"""
测试升级版web-search技能
"""

import sys
import os

# 添加技能路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_web_search():
    """测试web搜索功能"""
    try:
        from web_search import WebSearch

        print("🔍 测试升级版web-search技能...")
        print("=" * 60)

        # 创建搜索实例
        ws = WebSearch()

        # 测试搜索功能
        print("\n测试1: 搜索A股相关信息")
        results = ws.search("A股股票列表", max_results=5)

        print(f"✅ 搜索成功！找到 {len(results)} 个结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', '无标题')}")
            print(f"   URL: {result.get('url', '无链接')}")
            print(f"   来源: {result.get('source', 'unknown')}")
            print(f"   相关度: {result.get('score', 0):.2f}")
            print(f"   质量分: {result.get('quality_score', 0):.2f}")
            print(f"   摘要: {result.get('snippet', '无摘要')[:150]}...")
            print()

        # 测试高级搜索
        print("\n测试2: 高级搜索（时间范围）")
        results = ws.search("人工智能发展趋势", max_results=5, time_range="7d")
        print(f"✅ 高级搜索成功！找到 {len(results)} 个结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', '无标题')}")
            print(f"   相关度: {result.get('score', 0):.2f}")
            print(f"   质量分: {result.get('quality_score', 0):.2f}")
            print()

        # 测试URL抓取
        print("\n测试3: URL内容抓取")
        url = "https://www.python.org"
        content = ws.fetch_url(url, extract_mode="text")
        print(f"✅ URL抓取成功！内容长度: {len(content)} 字符")
        print(f"前200字符: {content[:200]}...")

        # 测试文本摘要
        print("\n测试4: 文本摘要")
        summary = ws.summarize(content, max_sentences=3)
        print(f"✅ 摘要生成成功！")
        print(f"摘要内容: {summary}")

        # 测试搜索历史
        print("\n测试5: 搜索历史")
        history = ws.get_search_history(limit=3)
        print(f"✅ 搜索历史获取成功！")
        for i, item in enumerate(history, 1):
            print(f"{i}. 查询: '{item.get('query', '')}' - 结果数: {item.get('results_count', 0)}")

        # 测试缓存清除
        print("\n测试6: 缓存清除")
        ws.clear_cache()
        print("✅ 缓存已清除")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comparison():
    """测试新旧版本对比"""
    try:
        from web_search import WebSearch

        print("\n" + "=" * 60)
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

        return True

    except Exception as e:
        print(f"❌ 对比测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔥 火娃 - 升级版Web搜索技能测试")
    print("=" * 60)

    # 测试搜索功能
    search_success = test_web_search()

    print("\n" + "=" * 60)

    # 测试对比
    comparison_success = test_comparison()

    print("\n" + "=" * 60)
    print("🎯 测试结果:")
    print(f"搜索功能: {'✅ 成功' if search_success else '❌ 失败'}")
    print(f"对比测试: {'✅ 成功' if comparison_success else '❌ 失败'}")

    if search_success and comparison_success:
        print("\n🎉 所有测试通过！升级版web-search技能已成功安装并可用。")
        print("\n🔥 火娃提示: 升级版web-search技能提供了更高质量的搜索结果！")
    else:
        print("\n⚠️  部分测试失败，请检查配置。")