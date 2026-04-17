#!/usr/bin/env python3
"""
Web搜索技能演示脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from web_search import WebSearch
    ws = WebSearch()
    print("✅ Web搜索模块导入成功！")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def demo_search():
    """演示搜索功能"""
    print("\n🔍 演示搜索功能...")
    
    # 搜索查询
    query = "人工智能发展趋势"
    print(f"搜索查询: {query}")
    
    try:
        # 执行搜索
        results = ws.search(query, max_results=3)
        
        print(f"📊 搜索结果 ({len(results)} 个):")
        print("-" * 50)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 标题: {result.get('title', '无标题')}")
            print(f"   URL: {result.get('url', '无链接')}")
            print(f"   摘要: {result.get('snippet', '无摘要')[:100]}...")
            print()
            
    except Exception as e:
        print(f"❌ 搜索失败: {e}")

def demo_url_fetch():
    """演示URL抓取功能"""
    print("\n📄 演示URL抓取功能...")
    
    # 测试URL
    url = "https://www.python.org"
    print(f"抓取URL: {url}")
    
    try:
        # 抓取内容
        content = ws.fetch_url(url, extract_mode="text", max_chars=500)
        
        print(f"📝 抓取内容 (前500字符):")
        print("-" * 50)
        print(content)
        print()
        
    except Exception as e:
        print(f"❌ URL抓取失败: {e}")

def demo_summary():
    """演示摘要功能"""
    print("\n📝 演示摘要功能...")
    
    # 示例文本
    sample_text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    人工智能技术包括机器学习、深度学习、自然语言处理、计算机视觉等多个领域。
    近年来，人工智能技术取得了飞速发展，在医疗、金融、交通、教育等各个领域都有广泛应用。
    人工智能的发展将深刻改变人类的生活方式，推动社会进步。
    """
    
    print("原始文本:")
    print("-" * 30)
    print(sample_text)
    
    try:
        # 生成摘要
        summary = ws.summarize(sample_text, max_sentences=2)
        
        print("\n摘要:")
        print("-" * 30)
        print(summary)
        
    except Exception as e:
        print(f"❌ 摘要生成失败: {e}")

def demo_export():
    """演示导出功能"""
    print("\n💾 演示导出功能...")
    
    # 创建示例搜索结果
    sample_results = [
        {
            'title': '人工智能发展趋势分析',
            'url': 'https://example.com/ai-trends',
            'snippet': '人工智能技术在各个领域的应用和发展趋势分析...'
        },
        {
            'title': '机器学习最新进展',
            'url': 'https://example.com/ml-progress',
            'snippet': '机器学习算法的最新研究进展和应用案例...'
        }
    ]
    
    try:
        # 导出为CSV
        success = ws.export_results(sample_results, format="csv", filename="demo_results.csv")
        
        if success:
            print("✅ CSV导出成功！")
            print(f"文件: demo_results.csv")
        
        # 导出为JSON
        success = ws.export_results(sample_results, format="json", filename="demo_results.json")
        
        if success:
            print("✅ JSON导出成功！")
            print(f"文件: demo_results.json")
            
    except Exception as e:
        print(f"❌ 导出失败: {e}")

def main():
    """主演示函数"""
    print("🔥 火娃 - Web搜索技能演示")
    print("=" * 60)
    
    # 演示各项功能
    demo_search()
    demo_url_fetch()
    demo_summary()
    demo_export()
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！")
    print("💡 提示: 如果搜索功能因网络问题无法使用，URL抓取和本地功能仍然可用。")

if __name__ == "__main__":
    main()