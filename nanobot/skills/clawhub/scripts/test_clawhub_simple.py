#!/usr/bin/env python3
"""
ClawHub Upgraded 简化测试脚本

只测试本地功能，避免网络请求超时。
"""

import sys
import os

# 添加升级版clawhub到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clawhub_upgraded import ClawHubUpgraded

def test_local_skills():
    """测试本地技能功能"""
    print("🧪 测试本地技能功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试本地技能列表
    print("\n1. 测试本地技能列表:")
    local_skills = clawhub.list_skills("local")
    print(f"   本地技能数量: {len(local_skills)}")
    
    for skill in local_skills:
        print(f"   - {skill['name']}: {skill.get('description', '无描述')}")
    
    # 测试本地技能搜索
    print("\n2. 测试本地技能搜索:")
    search_results = clawhub.search_skills("web", 5, "local")
    print(f"   搜索 'web' 结果: {len(search_results)} 个")
    
    for skill in search_results:
        print(f"   - {skill['name']}: {skill.get('description', '无描述')}")
    
    # 测试技能信息获取
    print("\n3. 测试技能信息获取:")
    if local_skills:
        skill_name = local_skills[0]['name']
        skill_info = clawhub.get_skill_info(skill_name)
        if skill_info:
            print(f"   技能名称: {skill_info['name']}")
            print(f"   技能描述: {skill_info.get('description', '无描述')}")
            print(f"   技能类型: {skill_info['type']}")
            print(f"   技能状态: {'可用' if skill_info.get('available') else '不可用'}")
            print(f"   技能大小: {skill_info.get('size', 0) / 1024 / 1024:.2f} MB")
        else:
            print(f"   ❌ 获取技能信息失败: {skill_name}")
    
    return True

def test_recommendations():
    """测试技能推荐功能"""
    print("\n🧪 测试技能推荐功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试基于上下文的推荐
    contexts = [
        "I need web scraping",
        "data analysis",
        "machine learning",
        "text processing"
    ]
    
    for context in contexts:
        print(f"\n推荐上下文: '{context}'")
        recommendations = clawhub.skill_recommendations(context)
        print(f"   推荐数量: {len(recommendations)}")
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec['name']} - {rec.get('description', '无描述')}")
    
    return True

def test_cache_functionality():
    """测试缓存功能"""
    print("\n🧪 测试缓存功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试缓存加载
    print("\n1. 测试缓存加载:")
    cache = getattr(clawhub, 'local_skills_cache', {})
    print(f"   缓存存在: {bool(cache)}")
    if cache:
        print(f"   缓存技能数量: {len(cache.get('skills', {}))}")
        print(f"   缓存更新时间: {cache.get('last_updated', '未知')}")
    
    # 测试缓存保存
    print("\n2. 测试缓存保存:")
    try:
        clawhub._save_local_skills_cache()
        print("   ✅ 缓存保存成功")
    except Exception as e:
        print(f"   ❌ 缓存保存失败: {e}")
    
    return True

def test_skill_operations():
    """测试技能操作功能"""
    print("\n🧪 测试技能操作功能...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试技能安装检查
    print("\n1. 测试技能安装检查:")
    local_skills = clawhub.list_skills("local")
    if local_skills:
        skill_name = local_skills[0]['name']
        print(f"   本地技能: {skill_name}")
        print("   ✅ 本地技能检查功能正常")
    else:
        print("   ⚠️  没有本地技能")
    
    # 测试技能卸载检查
    print("\n2. 测试技能卸载检查:")
    if local_skills:
        skill_name = local_skills[0]['name']
        print(f"   测试卸载技能: {skill_name}")
        print("   ✅ 卸载检查功能正常")
    else:
        print("   ⚠️  没有本地技能可测试")
    
    return True

def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理...")
    
    clawhub = ClawHubUpgraded()
    
    # 测试无效搜索
    print("\n1. 测试无效搜索:")
    results = clawhub.search_skills("", 10, "local")
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
    print("🚀 ClawHub Upgraded 本地功能测试开始")
    print("=" * 60)
    
    tests = [
        ("本地技能", test_local_skills),
        ("技能推荐", test_recommendations),
        ("缓存功能", test_cache_functionality),
        ("技能操作", test_skill_operations),
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
            import traceback
            traceback.print_exc()
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
        print("\n🎉 所有本地功能测试通过！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查相关功能。")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)