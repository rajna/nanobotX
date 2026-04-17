#!/usr/bin/env python3
"""
ClawHub: 简化的技能搜索和管理接口

这个脚本提供了用户友好的技能搜索和管理功能。
"""

import sys
import os

# 添加升级版clawhub到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clawhub_upgraded import ClawHubUpgraded

def search_skills(query, limit=10, search_type='all'):
    """搜索技能"""
    clawhub = ClawHubUpgraded()
    results = clawhub.search_skills(query, limit, search_type)
    
    print(f"\n🔍 搜索结果: '{query}'")
    print("=" * 60)
    
    if not results:
        print("❌ 未找到相关技能")
        return
    
    for i, skill in enumerate(results, 1):
        print(f"{i}. {skill['name']}")
        print(f"   📝 {skill.get('description', '无描述')}")
        print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
        
        if skill.get('installed'):
            print(f"   ✅ 已安装")
        elif skill.get('installable'):
            print(f"   📦 可安装")
        
        if skill.get('search_score'):
            print(f"   ⭐ 相关度: {skill['search_score']}")
        
        print()

def install_skill(skill_name, force=False):
    """安装技能"""
    clawhub = ClawHubUpgraded()
    result = clawhub.install_skill(skill_name, force)
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")

def list_skills(skill_type='all'):
    """列出技能"""
    clawhub = ClawHubUpgraded()
    skills = clawhub.list_skills(skill_type)
    
    print(f"\n📋 技能列表 (类型: {skill_type})")
    print("=" * 60)
    
    if not skills:
        print("❌ 未找到技能")
        return
    
    for skill in skills:
        print(f"📦 {skill['name']}")
        print(f"   📝 {skill.get('description', '无描述')}")
        print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
        print(f"   ✅ 状态: {'可用' if skill.get('available') else '不可用'}")
        
        size_mb = skill.get('size', 0) / (1024 * 1024)
        if size_mb > 0:
            print(f"   📁 大小: {size_mb:.2f} MB")
        
        print()

def get_skill_info(skill_name):
    """获取技能信息"""
    clawhub = ClawHubUpgraded()
    skill_info = clawhub.get_skill_info(skill_name)
    
    if not skill_info:
        print(f"❌ 未找到技能: {skill_name}")
        return
    
    print(f"\n📋 技能信息: {skill_name}")
    print("=" * 60)
    
    print(f"📝 {skill_info.get('description', '无描述')}")
    print(f"🏷️ 类型: {skill_info.get('type', 'unknown')}")
    print(f"📍 路径: {skill_info.get('path', 'Unknown')}")
    print(f"✅ 状态: {'可用' if skill_info.get('available') else '不可用'}")
    
    if skill_info.get('installed_at'):
        print(f"📅 安装时间: {skill_info['installed_at']}")
    
    size_mb = skill_info.get('size', 0) / (1024 * 1024)
    if size_mb > 0:
        print(f"📁 大小: {size_mb:.2f} MB")
    
    print()

def recommend_skills(context=''):
    """推荐技能"""
    clawhub = ClawHubUpgraded()
    recommendations = clawhub.skill_recommendations(context)
    
    print(f"\n🎯 技能推荐 (基于: '{context}')")
    print("=" * 60)
    
    if not recommendations:
        print("❌ 未找到推荐的技能")
        return
    
    for i, skill in enumerate(recommendations, 1):
        print(f"{i}. {skill['name']}")
        print(f"   📝 {skill.get('description', '无描述')}")
        print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
        
        if skill.get('installed'):
            print(f"   ✅ 已安装")
        elif skill.get('installable'):
            print(f"   📦 可安装")
        
        print()

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
ClawHub: 升级版的技能搜索和管理系统

用法:
    python clawhub.py <action> [options]

Actions:
    search <query> [limit] [type]      搜索技能
    install <skill_name> [force]        安装技能
    list [type]                        列出技能
    info <skill_name>                  获取技能信息
    recommend [context]                 推荐技能

示例:
    python clawhub.py search web scraping 10 all
    python clawhub.py install web-scraper --force
    python clawhub.py list local
    python clawhub.py info web-search
    python clawhub.py recommend "I need data analysis"
        """)
        return
    
    action = sys.argv[1]
    
    if action == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else ''
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        search_type = sys.argv[4] if len(sys.argv) > 4 else 'all'
        search_skills(query, limit, search_type)
        
    elif action == 'install':
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ''
        force = '--force' in sys.argv
        install_skill(skill_name, force)
        
    elif action == 'list':
        skill_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
        list_skills(skill_type)
        
    elif action == 'info':
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ''
        get_skill_info(skill_name)
        
    elif action == 'recommend':
        context = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        recommend_skills(context)
        
    else:
        print(f"❌ 未知操作: {action}")

if __name__ == '__main__':
    main()