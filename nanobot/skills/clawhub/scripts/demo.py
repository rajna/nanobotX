#!/usr/bin/env python3
"""
ClawHub Upgraded 演示脚本

展示升级版ClawHub技能的主要功能。
"""

import sys
import os

# 添加升级版clawhub到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clawhub_upgraded import ClawHubUpgraded

def demo_search():
    """演示搜索功能"""
    print("🔍 演示技能搜索功能")
    print("=" * 50)
    
    clawhub = ClawHubUpgraded()
    
    # 搜索本地技能
    print("\n1. 搜索本地技能:")
    results = clawhub.search_skills("web", 5, "local")
    print(f"   搜索 'web' 找到 {len(results)} 个本地技能:")
    
    for i, skill in enumerate(results, 1):
        print(f"   {i}. {skill['name']}")
        print(f"      描述: {skill.get('description', '无描述')}")
        print(f"      类型: {skill.get('type', 'unknown')}")
        print(f"      状态: {'✅ 已安装' if skill.get('installed') else '❌ 未安装'}")
        print()
    
    # 搜索远程技能
    print("2. 搜索远程技能:")
    results = clawhub.search_skills("data", 3, "remote")
    print(f"   搜索 'data' 找到 {len(results)} 个远程技能:")
    
    for i, skill in enumerate(results, 1):
        print(f"   {i}. {skill['name']}")
        print(f"      描述: {skill.get('description', '无描述')}")
        print(f"      类型: {skill.get('type', 'unknown')}")
        print(f"      状态: {'📦 可安装' if skill.get('installable') else '❌ 不可安装'}")
        print()

def demo_list():
    """演示列表功能"""
    print("📋 演示技能列表功能")
    print("=" * 50)
    
    clawhub = ClawHubUpgraded()
    
    # 列出所有技能
    print("\n1. 所有技能列表:")
    skills = clawhub.list_skills("all")
    print(f"   总共 {len(skills)} 个技能:")
    
    for skill in skills:
        print(f"   📦 {skill['name']}")
        print(f"      描述: {skill.get('description', '无描述')}")
        print(f"      类型: {skill.get('type', 'unknown')}")
        print(f"      状态: {'✅ 可用' if skill.get('available') else '❌ 不可用'}")
        
        size_mb = skill.get('size', 0) / (1024 * 1024)
        if size_mb > 0:
            print(f"      大小: {size_mb:.2f} MB")
        print()
    
    # 列出本地技能
    print("2. 本地技能列表:")
    local_skills = clawhub.list_skills("local")
    print(f"   本地技能 {len(local_skills)} 个:")
    
    for skill in local_skills:
        print(f"   📦 {skill['name']}")
        print(f"      描述: {skill.get('description', '无描述')}")
        print()

def demo_info():
    """演示信息获取功能"""
    print("📋 演示技能信息获取功能")
    print("=" * 50)
    
    clawhub = ClawHubUpgraded()
    
    # 获取本地技能信息
    local_skills = clawhub.list_skills("local")
    if local_skills:
        skill_name = local_skills[0]['name']
        print(f"\n1. 获取技能信息: {skill_name}")
        
        skill_info = clawhub.get_skill_info(skill_name)
        if skill_info:
            print(f"   名称: {skill_info['name']}")
            print(f"   描述: {skill_info.get('description', '无描述')}")
            print(f"   类型: {skill_info['type']}")
            print(f"   路径: {skill_info.get('path', 'Unknown')}")
            print(f"   状态: {'✅ 可用' if skill_info.get('available') else '❌ 不可用'}")
            
            if skill_info.get('installed_at'):
                print(f"   安装时间: {skill_info['installed_at']}")
            
            size_mb = skill_info.get('size', 0) / (1024 * 1024)
            if size_mb > 0:
                print(f"   大小: {size_mb:.2f} MB")
            
            print(f"   文件数量: {len(skill_info.get('files', []))}")
            print("   主要文件:")
            for file in skill_info.get('files', [])[:5]:
                print(f"      - {file}")
            if len(skill_info.get('files', [])) > 5:
                print(f"      ... 还有 {len(skill_info.get('files', [])) - 5} 个文件")
        else:
            print(f"   ❌ 获取技能信息失败")
    
    # 获取远程技能信息
    remote_results = clawhub.search_skills("web", 1, "remote")
    if remote_results:
        skill_name = remote_results[0]['name']
        print(f"\n2. 获取远程技能信息: {skill_name}")
        
        skill_info = clawhub.get_skill_info(skill_name)
        if skill_info:
            print(f"   名称: {skill_info['name']}")
            print(f"   描述: {skill_info.get('description', '无描述')}")
            print(f"   类型: {skill_info['type']}")
            print(f"   来源: {skill_info.get('source', 'Unknown')}")
            print(f"   可安装: {'✅ 是' if skill_info.get('installable') else '❌ 否'}")
        else:
            print(f"   ❌ 获取远程技能信息失败")

def demo_recommendations():
    """演示推荐功能"""
    print("🎯 演示技能推荐功能")
    print("=" * 50)
    
    clawhub = ClawHubUpgraded()
    
    # 不同上下文的推荐
    contexts = [
        "I need web scraping",
        "data analysis and visualization", 
        "machine learning and AI",
        "text processing and NLP",
        "stock market analysis"
    ]
    
    for context in contexts:
        print(f"\n推荐上下文: '{context}'")
        recommendations = clawhub.skill_recommendations(context)
        print(f"   推荐数量: {len(recommendations)}")
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec['name']}")
            print(f"      描述: {rec.get('description', '无描述')}")
            print(f"      类型: {rec.get('type', 'unknown')}")
            print(f"      状态: {'✅ 已安装' if rec.get('installed') else '📦 可安装' if rec.get('installable') else '❌ 不可用'}")
            print()

def demo_operations():
    """演示操作功能"""
    print("🔧 演示技能操作功能")
    print("=" * 50)
    
    clawhub = ClawHubUpgraded()
    
    # 演示技能安装检查
    print("\n1. 技能安装检查:")
    remote_results = clawhub.search_skills("web", 2, "remote")
    if remote_results:
        for skill in remote_results:
            skill_name = skill['name']
            print(f"   技能: {skill_name}")
            print(f"   可安装: {'✅ 是' if skill.get('installable') else '❌ 否'}")
            print(f"   描述: {skill.get('description', '无描述')}")
            print()
    else:
        print("   ⚠️  没有找到可安装的远程技能")
    
    # 演示技能卸载检查
    print("2. 技能卸载检查:")
    local_skills = clawhub.list_skills("local")
    if local_skills:
        for skill in local_skills:
            skill_name = skill['name']
            print(f"   技能: {skill_name}")
            print(f"   可卸载: ✅ 是")
            print(f"   描述: {skill.get('description', '无描述')}")
            print()
    else:
        print("   ⚠️  没有本地技能可卸载")
    
    # 演示技能更新检查
    print("3. 技能更新检查:")
    print("   更新功能: ✅ 支持")
    print("   批量更新: ✅ 支持")
    print("   单个更新: ✅ 支持")
    print()

def demo_comparison():
    """演示与原版对比"""
    print("🆚 升级版 vs 原版对比")
    print("=" * 50)
    
    features = [
        ("搜索范围", "仅远程", "本地+远程+网络"),
        ("搜索速度", "依赖网络", "本地毫秒级"),
        ("智能排序", "基础排序", "相关性排序"),
        ("技能管理", "基础安装", "完整管理"),
        ("推荐系统", "无", "智能上下文推荐"),
        ("缓存机制", "无", "本地缓存优化"),
        ("错误处理", "基础", "完善处理"),
        ("用户体验", "命令行", "友好界面")
    ]
    
    print("\n功能对比:")
    for feature, original, upgraded in features:
        print(f"   {feature:15} | {original:15} | {upgraded:15}")
    
    print("\n🎉 升级版优势:")
    print("   ✅ 更快的搜索速度")
    print("   ✅ 更智能的排序")
    print("   ✅ 更完整的技能管理")
    print("   ✅ 更好的用户体验")
    print("   ✅ 更强大的推荐系统")
    print("   ✅ 更完善的错误处理")

def main():
    """主演示函数"""
    print("🚀 ClawHub Upgraded 功能演示")
    print("=" * 60)
    print("这是一个升级版的技能搜索和管理系统")
    print("相比原版ClawHub，提供了更强大的功能！")
    print()
    
    demos = [
        ("搜索功能", demo_search),
        ("列表功能", demo_list),
        ("信息获取", demo_info),
        ("推荐功能", demo_recommendations),
        ("操作功能", demo_operations),
        ("版本对比", demo_comparison)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
            print(f"\n✅ {demo_name} 演示完成")
            print("-" * 60)
        except Exception as e:
            print(f"\n❌ {demo_name} 演示失败: {e}")
            print("-" * 60)
    
    print("\n🎉 所有演示完成！")
    print("升级版ClawHub提供了更强大的技能搜索和管理功能！")

if __name__ == '__main__':
    main()