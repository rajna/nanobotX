#!/usr/bin/env python3
"""
测试web-search技能
"""

import sys
import os

# 添加技能路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_web_search():
    """测试web搜索功能"""
    try:
        # 导入web_search模块
        import web_search
        
        print("🔍 测试web搜索技能...")
        
        # 测试搜索功能
        results = web_search.search("Python编程教程", max_results=3)
        
        print(f"✅ 搜索成功！找到 {len(results)} 个结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', '无标题')}")
            print(f"   URL: {result.get('url', '无链接')}")
            print(f"   摘要: {result.get('snippet', '无摘要')[:100]}...")
            print()
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_url_fetch():
    """测试URL内容抓取功能"""
    try:
        import web_search
        
        print("📄 测试URL内容抓取...")
        
        # 测试抓取网页内容
        url = "https://www.python.org"
        content = web_search.fetch_url(url, extract_mode="text")
        
        print(f"✅ URL抓取成功！内容长度: {len(content)} 字符")
        print(f"前200字符: {content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ URL抓取测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🔥 火娃 - Web搜索技能测试")
    print("=" * 50)
    
    # 测试搜索功能
    search_success = test_web_search()
    
    print("\n" + "=" * 50)
    
    # 测试URL抓取功能
    fetch_success = test_url_fetch()
    
    print("\n" + "=" * 50)
    print("🎯 测试结果:")
    print(f"搜索功能: {'✅ 成功' if search_success else '❌ 失败'}")
    print(f"URL抓取: {'✅ 成功' if fetch_success else '❌ 失败'}")
    
    if search_success and fetch_success:
        print("\n🎉 所有测试通过！web-search技能已成功安装并可用。")
    else:
        print("\n⚠️  部分测试失败，请检查配置。")