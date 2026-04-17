#!/usr/bin/env python3
"""
ClawHub Upgraded: 升级版的技能搜索和管理系统

这个脚本提供了更强大的技能搜索、管理和安装功能，完全集成到nanobot系统中。
"""

import os
import sys
import json
import re
import subprocess
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import shutil
import tempfile

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from web_search import WebSearch
    from sentiment_analyzer import SentimentAnalyzer
except ImportError:
    print("⚠️  依赖模块未找到，将使用基础功能")
    WebSearch = None
    SentimentAnalyzer = None

class ClawHubUpgraded:
    """升级版的ClawHub技能管理器"""
    
    def __init__(self, skills_dir: str = None):
        self.skills_dir = skills_dir or os.path.expanduser('~/.nanobot/workspace/skills')
        self.web_search = WebSearch() if WebSearch else None
        self.sentiment_analyzer = SentimentAnalyzer() if SentimentAnalyzer else None
        
        # 确保技能目录存在
        os.makedirs(self.skills_dir, exist_ok=True)
        
        # 本地技能缓存
        self.local_skills_cache = {}
        self._load_local_skills()
    
    def _load_local_skills(self):
        """加载本地技能信息"""
        try:
            if os.path.exists(os.path.join(self.skills_dir, '.skills_cache.json')):
                with open(os.path.join(self.skills_dir, '.skills_cache.json'), 'r', encoding='utf-8') as f:
                    self.local_skills_cache = json.load(f)
            else:
                self._scan_local_skills()
        except Exception as e:
            print(f"⚠️  加载本地技能缓存失败: {e}")
            self._scan_local_skills()
    
    def _scan_local_skills(self):
        """扫描本地技能目录"""
        self.local_skills_cache = {
            'last_updated': datetime.now().isoformat(),
            'skills': {}
        }
        
        if not os.path.exists(self.skills_dir):
            return
        
        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            
            if os.path.isdir(skill_path):
                skill_info = self._analyze_skill_directory(skill_path)
                if skill_info:
                    self.local_skills_cache['skills'][skill_name] = skill_info
        
        # 保存缓存
        self._save_local_skills_cache()
    
    def _analyze_skill_directory(self, skill_path: str) -> Optional[Dict]:
        """分析技能目录"""
        try:
            skill_info = {
                'name': os.path.basename(skill_path),
                'path': skill_path,
                'type': 'local',
                'installed_at': datetime.fromtimestamp(os.path.getctime(skill_path)).isoformat(),
                'updated_at': datetime.fromtimestamp(os.path.getmtime(skill_path)).isoformat(),
                'size': self._get_directory_size(skill_path),
                'files': [],
                'description': '',
                'dependencies': [],
                'available': True
            }
            
            # 扫描技能文件
            for root, dirs, files in os.walk(skill_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, skill_path)
                    skill_info['files'].append(rel_path)
                    
                    # 读取技能描述
                    if file == 'SKILL.md':
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # 提取description
                            desc_match = re.search(r'description:\s*"([^"]*)"', content)
                            if desc_match:
                                skill_info['description'] = desc_match.group(1)
                        except:
                            pass
            
            # 检查技能是否可用
            skill_info['available'] = self._check_skill_availability(skill_path)
            
            return skill_info
            
        except Exception as e:
            print(f"⚠️  分析技能目录失败 {skill_path}: {e}")
            return None
    
    def _get_directory_size(self, path: str) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        except:
            pass
        return total_size
    
    def _check_skill_availability(self, skill_path: str) -> bool:
        """检查技能是否可用"""
        try:
            # 检查是否有SKILL.md文件
            skill_md = os.path.join(skill_path, 'SKILL.md')
            if not os.path.exists(skill_md):
                return False
            
            # 检查是否有scripts目录
            scripts_dir = os.path.join(skill_path, 'scripts')
            if not os.path.exists(scripts_dir):
                return False
            
            return True
        except:
            return False
    
    def _save_local_skills_cache(self):
        """保存本地技能缓存"""
        try:
            with open(os.path.join(self.skills_dir, '.skills_cache.json'), 'w', encoding='utf-8') as f:
                json.dump(self.local_skills_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  保存本地技能缓存失败: {e}")
    
    def search_skills(self, query: str, limit: int = 10, search_type: str = 'all') -> List[Dict]:
        """搜索技能"""
        print(f"🔍 正在搜索技能: '{query}' (类型: {search_type}, 限制: {limit})")
        
        results = []
        
        # 1. 搜索本地技能
        if search_type in ['all', 'local']:
            local_results = self._search_local_skills(query, limit)
            results.extend(local_results)
        
        # 2. 搜索远程技能
        if search_type in ['all', 'remote']:
            remote_results = self._search_remote_skills(query, limit)
            results.extend(remote_results)
        
        # 3. 搜索网络技能
        if search_type in ['all', 'web'] and self.web_search:
            web_results = self._search_web_skills(query, limit)
            results.extend(web_results)
        
        # 去重和排序
        unique_results = self._deduplicate_skills(results)
        sorted_results = self._sort_skills_by_relevance(unique_results, query)
        
        return sorted_results[:limit]
    
    def _search_local_skills(self, query: str, limit: int) -> List[Dict]:
        """搜索本地技能"""
        results = []
        query_lower = query.lower()
        
        for skill_name, skill_info in self.local_skills_cache.get('skills', {}).items():
            score = 0
            
            # 名称匹配
            if query_lower in skill_name.lower():
                score += 10
            
            # 描述匹配
            if skill_info.get('description', '').lower():
                if query_lower in skill_info['description'].lower():
                    score += 8
            
            # 文件内容匹配
            for file_path in skill_info.get('files', []):
                if query_lower in file_path.lower():
                    score += 5
            
            if score > 0:
                skill_info['search_score'] = score
                skill_info['search_type'] = 'local'
                results.append(skill_info)
        
        return results
    
    def _search_remote_skills(self, query: str, limit: int) -> List[Dict]:
        """搜索远程技能（使用ClawHub CLI）"""
        results = []
        
        try:
            # 使用ClawHub CLI搜索
            cmd = ['npx', '--yes', 'clawhub@latest', 'search', query, '--limit', str(limit)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # 解析ClawHub输出
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Searching'):
                        skill_info = self._parse_clawhub_output(line)
                        if skill_info:
                            skill_info['search_score'] = 7  # 远程技能基础分
                            skill_info['search_type'] = 'remote'
                            results.append(skill_info)
            
        except subprocess.TimeoutExpired:
            print("⚠️  ClawHub搜索超时")
        except Exception as e:
            print(f"⚠️  ClawHub搜索失败: {e}")
        
        return results
    
    def _parse_clawhub_output(self, line: str) -> Optional[Dict]:
        """解析ClawHub输出"""
        try:
            # 示例行: "🦞 web-scraper - Web scraping and data extraction"
            parts = line.split(' - ', 1)
            if len(parts) == 2:
                name_part = parts[0].strip()
                desc_part = parts[1].strip()
                
                # 提取名称（移除emoji）
                name = re.sub(r'^[\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', '', name_part)
                
                return {
                    'name': name,
                    'description': desc_part,
                    'type': 'remote',
                    'source': 'clawhub',
                    'installable': True,
                    'installed': False
                }
        except:
            pass
        
        return None
    
    def _search_web_skills(self, query: str, limit: int) -> List[Dict]:
        """通过网络搜索技能"""
        if not self.web_search:
            return []
        
        results = []
        
        try:
            # 搜索技能相关内容
            search_queries = [
                f'AI agent skills {query}',
                f'nanobot skills {query}',
                f'AI assistant skills {query}'
            ]
            
            for search_query in search_queries:
                search_results = self.web_search.search(search_query, count=5)
                
                for result in search_results:
                    skill_info = {
                        'name': result.get('name', 'Unknown Skill'),
                        'description': result.get('snippet', 'No description available'),
                        'type': 'web',
                        'source': 'web_search',
                        'url': result.get('url', ''),
                        'installable': False,
                        'installed': False,
                        'search_score': 3  # 网络搜索基础分
                    }
                    results.append(skill_info)
        
        except Exception as e:
            print(f"⚠️  网络技能搜索失败: {e}")
        
        return results
    
    def _deduplicate_skills(self, skills: List[Dict]) -> List[Dict]:
        """技能去重"""
        seen_names = set()
        unique_skills = []
        
        for skill in skills:
            name = skill.get('name', '')
            if name and name not in seen_names:
                seen_names.add(name)
                unique_skills.append(skill)
        
        return unique_skills
    
    def _sort_skills_by_relevance(self, skills: List[Dict], query: str) -> List[Dict]:
        """按相关性排序技能"""
        query_lower = query.lower()
        
        def calculate_relevance(skill):
            score = skill.get('search_score', 0)
            
            # 名称权重
            name = skill.get('name', '').lower()
            if query_lower in name:
                score += 5
            
            # 描述权重
            desc = skill.get('description', '').lower()
            if query_lower in desc:
                score += 3
            
            # 类型权重
            if skill.get('type') == 'local':
                score += 2  # 本地技能优先
            
            return score
        
        return sorted(skills, key=calculate_relevance, reverse=True)
    
    def install_skill(self, skill_name: str, force: bool = False) -> Dict:
        """安装技能"""
        print(f"📦 正在安装技能: {skill_name}")
        
        # 检查是否已安装
        if skill_name in self.local_skills_cache.get('skills', {}) and not force:
            return {
                'success': False,
                'message': f'技能 "{skill_name}" 已安装，使用 --force 强制重新安装'
            }
        
        # 尝试从ClawHub安装
        try:
            cmd = ['npx', '--yes', 'clawhub@latest', ' ']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # 重新扫描本地技能
                self._scan_local_skills()
                
                if skill_name in self.local_skills_cache.get('skills', {}):
                    return {
                        'success': True,
                        'message': f'技能 "{skill_name}" 安装成功',
                        'skill_info': self.local_skills_cache['skills'][skill_name]
                    }
                else:
                    return {
                        'success': False,
                        'message': f'技能 "{skill_name}" 安装失败，请检查技能名称'
                    }
            else:
                return {
                    'success': False,
                    'message': f'ClawHub安装失败: {result.stderr}'
                }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'message': '安装超时，请重试'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'安装失败: {e}'
            }
    
    def uninstall_skill(self, skill_name: str) -> Dict:
        """卸载技能"""
        print(f"🗑️  正在卸载技能: {skill_name}")
        
        if skill_name not in self.local_skills_cache.get('skills', {}):
            return {
                'success': False,
                'message': f'技能 "{skill_name}" 未安装'
            }
        
        try:
            skill_path = self.local_skills_cache['skills'][skill_name]['path']
            
            # 备份技能目录
            backup_path = os.path.join(self.skills_dir, f'{skill_name}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            shutil.move(skill_path, backup_path)
            
            # 重新扫描本地技能
            self._scan_local_skills()
            
            return {
                'success': True,
                'message': f'技能 "{skill_name}" 卸载成功，备份保存在: {backup_path}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'卸载失败: {e}'
            }
    
    def list_skills(self, skill_type: str = 'all') -> List[Dict]:
        """列出技能"""
        skills = []
        
        for skill_name, skill_info in self.local_skills_cache.get('skills', {}).items():
            if skill_type == 'all' or skill_info.get('type') == skill_type:
                skills.append(skill_info)
        
        return sorted(skills, key=lambda x: x.get('name', ''))
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        """获取技能详细信息"""
        if skill_name in self.local_skills_cache.get('skills', {}):
            return self.local_skills_cache['skills'][skill_name]
        
        # 搜索远程技能
        remote_skills = self._search_remote_skills(skill_name, 1)
        if remote_skills:
            return remote_skills[0]
        
        return None
    
    def update_skills(self, skill_names: List[str] = None) -> Dict:
        """更新技能"""
        print("🔄 正在更新技能...")
        
        if skill_names:
            # 更新指定技能
            results = []
            for skill_name in skill_names:
                result = self._update_single_skill(skill_name)
                results.append(result)
            return {'success': True, 'results': results}
        else:
            # 更新所有技能
            try:
                cmd = ['npx', '--yes', 'clawhub@latest', 'update', '--all', '--workdir', self.skills_dir]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    # 重新扫描本地技能
                    self._scan_local_skills()
                    return {
                        'success': True,
                        'message': '所有技能更新成功'
                    }
                else:
                    return {
                        'success': False,
                        'message': f'更新失败: {result.stderr}'
                    }
            
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'message': '更新超时，请重试'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'更新失败: {e}'
                }
    
    def _update_single_skill(self, skill_name: str) -> Dict:
        """更新单个技能"""
        try:
            # 卸载并重新安装
            uninstall_result = self.uninstall_skill(skill_name)
            if not uninstall_result['success']:
                return uninstall_result
            
            install_result = self.install_skill(skill_name, force=True)
            return install_result
        
        except Exception as e:
            return {
                'success': False,
                'message': f'更新技能 {skill_name} 失败: {e}'
            }
    
    def skill_recommendations(self, user_context: str = '') -> List[Dict]:
        """基于用户上下文推荐技能"""
        recommendations = []
        
        # 基于当前会话上下文推荐
        if 'web' in user_context.lower():
            recommendations.extend(self.search_skills('web scraping', 3))
        
        if 'data' in user_context.lower():
            recommendations.extend(self.search_skills('data analysis', 3))
        
        if 'ai' in user_context.lower() or 'ml' in user_context.lower():
            recommendations.extend(self.search_skills('machine learning', 3))
        
        if 'text' in user_context.lower():
            recommendations.extend(self.search_skills('text processing', 3))
        
        # 推荐热门技能
        if not recommendations:
            popular_skills = ['web-search', 'stock-query', 'sentiment-analyzer', 'memory']
            for skill_name in popular_skills:
                skill_info = self.get_skill_info(skill_name)
                if skill_info:
                    recommendations.append(skill_info)
        
        return recommendations[:5]

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
ClawHub Upgraded: 升级版的技能搜索和管理系统

用法:
    python clawhub_upgraded.py <action> [options]

Actions:
    search <query> [limit] [type]      搜索技能
    install <skill_name> [force]        安装技能
    uninstall <skill_name>              卸载技能
    list [type]                        列出技能
    info <skill_name>                  获取技能信息
    update [skill_names...]            更新技能
    recommend [context]                 推荐技能

示例:
    python clawhub_upgraded.py search web scraping 10 all
    python clawhub_upgraded.py install web-scraper --force
    python clawhub_upgraded.py list local
    python clawhub_upgraded.py update
    python clawhub_upgraded.py recommend "I need data analysis"
        """)
        return
    
    action = sys.argv[1]
    clawhub = ClawHubUpgraded()
    
    if action == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else ''
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        search_type = sys.argv[4] if len(sys.argv) > 4 else 'all'
        
        if not query:
            print("❌ 请提供搜索查询")
            return
        
        results = clawhub.search_skills(query, limit, search_type)
        
        print(f"\n🔍 搜索结果: '{query}'")
        print("=" * 60)
        
        for i, skill in enumerate(results, 1):
            print(f"{i}. {skill['name']}")
            print(f"   📝 描述: {skill.get('description', '无描述')}")
            print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
            print(f"   ⭐ 相关度: {skill.get('search_score', 0)}")
            
            if skill.get('installed'):
                print(f"   ✅ 已安装")
            elif skill.get('installable'):
                print(f"   📦 可安装")
            
            if skill.get('path'):
                size_mb = skill.get('size', 0) / (1024 * 1024)
                print(f"   📁 大小: {size_mb:.2f} MB")
            
            print()
    
    elif action == 'install':
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ''
        force = '--force' in sys.argv
        
        if not skill_name:
            print("❌ 请提供技能名称")
            return
        
        result = clawhub.install_skill(skill_name, force)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == 'uninstall':
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ''
        
        if not skill_name:
            print("❌ 请提供技能名称")
            return
        
        result = clawhub.uninstall_skill(skill_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == 'list':
        skill_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
        
        skills = clawhub.list_skills(skill_type)
        
        print(f"\n📋 技能列表 (类型: {skill_type})")
        print("=" * 60)
        
        if not skills:
            print("❌ 未找到技能")
            return
        
        for skill in skills:
            print(f"📦 {skill['name']}")
            print(f"   📝 描述: {skill.get('description', '无描述')}")
            print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
            print(f"   ✅ 状态: {'可用' if skill.get('available') else '不可用'}")
            
            if skill.get('installed_at'):
                install_date = skill['installed_at'][:10]
                print(f"   📅 安装时间: {install_date}")
            
            size_mb = skill.get('size', 0) / (1024 * 1024)
            print(f"   📁 大小: {size_mb:.2f} MB")
            print()
    
    elif action == 'info':
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ''
        
        if not skill_name:
            print("❌ 请提供技能名称")
            return
        
        skill_info = clawhub.get_skill_info(skill_name)
        
        if not skill_info:
            print(f"❌ 未找到技能: {skill_name}")
            return
        
        print(f"\n📋 技能信息: {skill_name}")
        print("=" * 60)
        
        print(f"📝 名称: {skill_info.get('name', 'Unknown')}")
        print(f"📋 描述: {skill_info.get('description', '无描述')}")
        print(f"🏷️ 类型: {skill_info.get('type', 'unknown')}")
        print(f"📍 路径: {skill_info.get('path', 'Unknown')}")
        print(f"✅ 状态: {'可用' if skill_info.get('available') else '不可用'}")
        
        if skill_info.get('installed_at'):
            print(f"📅 安装时间: {skill_info['installed_at']}")
        
        if skill_info.get('updated_at'):
            print(f"🔄 更新时间: {skill_info['updated_at']}")
        
        size_mb = skill_info.get('size', 0) / (1024 * 1024)
        print(f"📁 大小: {size_mb:.2f} MB")
        
        if skill_info.get('files'):
            print(f"📄 文件数量: {len(skill_info['files'])}")
            print("📁 主要文件:")
            for file in skill_info['files'][:10]:  # 只显示前10个文件
                print(f"   - {file}")
            if len(skill_info['files']) > 10:
                print(f"   ... 还有 {len(skill_info['files']) - 10} 个文件")
        
        print()
    
    elif action == 'update':
        skill_names = sys.argv[2:] if len(sys.argv) > 2 else None
        
        result = clawhub.update_skills(skill_names)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif action == 'recommend':
        context = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        
        recommendations = clawhub.skill_recommendations(context)
        
        print(f"\n🎯 技能推荐 (基于: '{context}')")
        print("=" * 60)
        
        if not recommendations:
            print("❌ 未找到推荐的技能")
            return
        
        for i, skill in enumerate(recommendations, 1):
            print(f"{i}. {skill['name']}")
            print(f"   📝 描述: {skill.get('description', '无描述')}")
            print(f"   🏷️ 类型: {skill.get('type', 'unknown')}")
            
            if skill.get('installed'):
                print(f"   ✅ 已安装")
            elif skill.get('installable'):
                print(f"   📦 可安装")
            
            print()
    
    else:
        print(f"❌ 未知操作: {action}")

if __name__ == '__main__':
    main()