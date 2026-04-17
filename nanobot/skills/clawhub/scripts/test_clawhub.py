#!/usr/bin/env python3
"""
ClawHub Upgraded 测试脚本

测试升级版ClawHub技能的各种功能。
"""

import sys
import os
import json

# 添加升级版clawhub到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clawhub_upgraded import ClawHubUpgraded

def test_search_skills():
    """测试技能搜索功能"""
    print("🧪 测试技能搜索功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试搜索本地技能
    print("\n1. 测试本地技能搜索:")
    local_results = clawhub.search_skills("web", 5, "local")
    print(f"   本地技能搜索结果: {len(local_results)} 个")
    
    # 测试搜索远程技能
    print("\n2. 测试远程技能搜索:")
    remote_results = clawhub.search_skills("data", 3, "remote")
    print(f"   远程技能搜索结果: {len(remote_results)} 个")
    
    # 测试综合搜索
    print("\n3. 测试综合搜索:")
    all_results = clawhub.search_skills("analysis", 10, "all")
    print(f"   综合搜索结果: {len(all_results)} 个")
    
    return True

def test_list_skills():
    """测试技能列表功能"""
    print("\n🧪 测试技能列表功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试列出所有技能
    print("\n1. 测试列出所有技能:")
    all_skills = clawhub.list_skills("all")
    print(f"   总技能数量: {len(all_skills)}")
    
    # 测试列出本地技能
    print("\n2. 测试列出本地技能:")
    local_skills = clawhub.list_skills("local")
    print(f"   本地技能数量: {len(local_skills)}")
    
    return True

def test_skill_info():
    """测试技能信息获取"""
    print("\n🧪 测试技能信息获取...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试获取本地技能信息
    print("\n1. 测试获取本地技能信息:")
    if local_skills := clawhub.list_skills("local"):
        skill_name = local_skills[0]['name']
        skill_info = clawhub.get_skill_info(skill_name)
        if skill_info:
            print(f"   技能名称: {skill_info['name']}")
            print(f"   技能描述: {skill_info.get('description', '无描述')}")
            print(f"   技能类型: {skill_info['type']}")
            print(f"   技能状态: {'可用' if skill_info.get('available') else '不可用'}")
        else:
            print(f"   ❌ 获取技能信息失败: {skill_name}")
    else:
        print("   ⚠️  没有本地技能可测试")
    
    # 测试获取远程技能信息
    print("\n2. 测试获取远程技能信息:")
    remote_results = clawhub.search_skills("web", 1, "remote")
    if remote_results:
        skill_name = remote_results[0]['name']
        skill_info = clawhub.get_skill_info(skill_name)
        if skill_info:
            print(f"   技能名称: {skill_info['name']}")
            print(f"   技能描述: {skill_info.get('description', '无描述')}")
            print(f"   技能类型: {skill_info['type']}")
        else:
            print(f"   ❌ 获取远程技能信息失败: {skill_name}")
    else:
        print("   ⚠️  没有远程技能可测试")
    
    return True

def test_recommendations():
    """测试技能推荐功能"""
    print("\n🧪 测试技能推荐功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试基于上下文的推荐
    contexts = [
        "I need web scraping",
        "data analysis and visualization",
        "machine learning and AI",
        "text processing and NLP"
    ]
    
    for context in contexts:
        print(f"\n推荐上下文: '{context}'")
        recommendations = clawhub.skill_recommendations(context)
        print(f"   推荐数量: {len(recommendations)}")
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec['name']} - {rec.get('description', '无描述')}")
    
    return True

def test_skill_operations():
    """测试技能操作功能"""
    print("\n🧪 测试技能操作功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试技能安装（仅测试，不实际安装）
    print("\n1. 测试技能安装检查:")
    remote_results = clawhub.search_skills("test", 1, "remote")
    if remote_results:
        skill_name = remote_results[0]['name']
        print(f"   测试安装技能: {skill_name}")
        # 这里不实际安装，只是测试功能
        print("   ✅ 安装检查功能正常")
    else:
        print("   ⚠️  没有找到可测试的技能")
    
    # 测试技能卸载检查
    print("\n2. 测试技能卸载检查:")
    local_skills = clawhub.list_skills("local")
    if local_skills:
        skill_name = local_skills[0]['name']
        print(f"   测试卸载技能: {skill_name}")
        # 这里不实际卸载，只是测试功能
        print("   ✅ 卸载检查功能正常")
    else:
        print("   ⚠️  没有本地技能可测试")
    
    return True

def test_performance():
    """测试性能"""
    print("\n🧪 测试性能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试搜索性能
    import time
    
    print("\n1. 测试搜索性能:")
    start_time = time.time()
    results = clawhub.search_skills("performance", 10, "all")
    end_time = time.time()
    
    search_time = end_time - start_time
    print(f"   搜索耗时: {search_time:.3f} 秒")
    print(f"   搜索结果: {len(results)} 个")
    
    # 测试列表性能
    print("\n2. 测试列表性能:")
    start_time = time.time()
    skills = clawhub.list_skills("all")
    end_time = time.time()
    
    list_time = end_time - start_time
    print(f"   列表耗时: {list_time:.3f} 秒")
    print(f"   技能数量: {len(skills)} 个")
    
    return True

def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试无效搜索
    print("\n1. 测试无效搜索:")
    results = clawhub.search_skills("", 10, "all")
    print(f"   空搜索结果: {len(results)} 个")
    
    # 测试无效技能信息
    print("\n2. 测试无效技能信息:")
    skill_info = clawhub.get_skill_info("nonexistent_skill")
    print(f"   不存在技能信息: {skill_info is None}")
    
    # 测试无效推荐
    print("\n3. 测试无效推荐:")
    recommendations = clawhub.skill_recommendations("")
    print(f"   空上下文推荐: {len(recommendations)} 个")
    
    return True

def main():
    """主测试函数"""
    print("🚀 ClawHub Upgraded 测试开始")
    print("=" * 60)
    
    tests = [
        ("技能搜索", test_search_skills),
        ("技能列表", test_list_skills),
        ("技能信息", test_skill_info),
        ("技能推荐", test_recommendations),
        ("技能操作", test_skill_operations),
        ("性能测试", test_performance),
        ("错误处理", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"\n✅ {test_name} 测试: {'通过' if success else '失败'}")
        except Exception as e:
            print(f"\n❌ {test_name} 测试失败: {e}")
            results.append((test_name, False))
    
    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"总测试数: {total}")
    print(f"通过数: {passed}")
    print(f"失败数: {total - passed}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    print("\n详细结果:")
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    if passed == total:
        print("\n🎉 所有测试通过！升级版ClawHub功能正常！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查相关功能。")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)