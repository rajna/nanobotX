---
name: clawhub-upgraded
description: "升级版的技能搜索和管理系统，提供强大的本地和远程技能搜索、安装、更新功能"
homepage: https://clawhub.ai
metadata: {"nanobot":{"emoji":"🦞🚀"}}
---

# ClawHub Upgraded

升级版的技能搜索和管理系统，完全集成到nanobot中，提供强大的技能发现、安装和管理功能。

## 🎯 主要特性

### 🔍 智能搜索
- **多源搜索**: 同时搜索本地、远程和网络技能
- **智能排序**: 基于相关性、类型、安装状态排序
- **模糊匹配**: 支持自然语言查询
- **实时缓存**: 本地技能信息缓存，快速响应

### 📦 完整管理
- **一键安装**: 支持从ClawHub安装技能
- **安全卸载**: 带备份的技能卸载功能
- **批量更新**: 支持单个或批量技能更新
- **详细信息**: 详细的技能信息和依赖分析

### 🎯 智能推荐
- **上下文推荐**: 基于用户对话内容推荐相关技能
- **热门推荐**: 推荐当前最热门的技能
- **个性化**: 根据使用历史推荐技能

## 🚀 使用方法

### 基本搜索

```bash
# 搜索技能
python clawhub.py search "web scraping" 10 all

# 搜索本地技能
python clawhub.py search "data analysis" 5 local

# 搜索远程技能
python clawhub.py search "machine learning" 3 remote
```

### 技能管理

```bash
# 安装技能
python clawhub.py install web-scraper

# 强制重新安装
python clawhub.py install web-scraper --force

# 卸载技能
python clawhub.py uninstall web-scraper

# 列出所有技能
python clawhub.py list

# 列出本地技能
python clawhub.py list local

# 获取技能详细信息
python clawhub.py info web-search
```

### 智能推荐

```bash
# 基于上下文推荐
python clawhub.py recommend "I need data analysis"

# 通用推荐
python clawhub.py recommend
```

### 技能更新

```bash
# 更新所有技能
python clawhub.py update

# 更新指定技能
python clawhub.py update web-scraper data-analyzer
```

## 📊 搜索类型

### 1. 本地技能搜索 (`local`)
- 扫描本地技能目录
- 基于名称、描述、文件内容匹配
- 显示安装状态和大小信息
- 优先级最高

### 2. 远程技能搜索 (`remote`)
- 通过ClawHub CLI搜索
- 显示可安装状态
- 包含技能描述和评分
- 支持一键安装

### 3. 网络技能搜索 (`web`)
- 通过网络搜索相关技能
- 显示技能链接和描述
- 提供发现新技能的途径
- 支持多种搜索引擎

## 🔧 高级功能

### 智能搜索算法

```python
# 相关性评分计算
def calculate_relevance(skill, query):
    score = skill.get('search_score', 0)
    
    # 名称匹配权重
    if query.lower() in skill['name'].lower():
        score += 5
    
    # 描述匹配权重
    if query.lower() in skill['description'].lower():
        score += 3
    
    # 类型权重
    if skill.get('type') == 'local':
        score += 2
    
    return score
```

### 技能缓存机制

```python
# 本地技能缓存结构
{
    "last_updated": "2026-03-11T15:30:00",
    "skills": {
        "web-search": {
            "name": "web-search",
            "description": "Web search and content extraction",
            "type": "local",
            "installed_at": "2026-03-10T10:00:00",
            "size": 1024000,
            "available": true,
            "files": ["SKILL.md", "scripts/web_search.py"]
        }
    }
}
```

### 推荐算法

```python
# 基于上下文的技能推荐
def skill_recommendations(self, user_context):
    recommendations = []
    
    # 关键词匹配
    if 'web' in user_context.lower():
        recommendations.extend(self.search_skills('web scraping', 3))
    
    if 'data' in user_context.lower():
        recommendations.extend(self.search_skills('data analysis', 3))
    
    # 热门技能推荐
    if not recommendations:
        popular_skills = ['web-search', 'stock-query', 'sentiment-analyzer']
        for skill_name in popular_skills:
            skill_info = self.get_skill_info(skill_name)
            if skill_info:
                recommendations.append(skill_info)
    
    return recommendations
```

## 📋 输出示例

### 搜索结果
```
🔍 搜索结果: 'web scraping'
============================================================
1. web-scraper
   📝 Web scraping and data extraction tool
   🏷️ 类型: remote
   📦 可安装
   ⭐ 相关度: 7

2. web-search
   📝 Advanced web search and content extraction
   🏷️ 类型: local
   ✅ 已安装
   ⭐ 相关度: 12

3. data-scraper
   📝 Data scraping and processing tool
   🏷️ 类型: remote
   📦 可安装
   ⭐ 相关度: 6
```

### 技能信息
```
📋 技能信息: web-search
============================================================
📝 Advanced web search and content extraction tool
🏷️ 类型: local
📍 路径: /Users/rama/.nanobot/workspace/skills/web-search
✅ 状态: 可用
📅 安装时间: 2026-03-10T10:00:00
📁 大小: 2.45 MB
📄 文件数量: 8
📁 主要文件:
   - SKILL.md
   - scripts/web_search.py
   - scripts/requirements.txt
   - scripts/test_search.py
   - ...
```

### 推荐结果
```
🎯 技能推荐 (基于: 'I need data analysis')
============================================================
1. data-analyzer
   📝 Advanced data analysis and visualization tool
   🏷️ 类型: remote
   📦 可安装

2. stock-query
   📝 A-share stock information query tool
   🏷️ 类型: local
   ✅ 已安装

3. sentiment-analyzer
   📝 Advanced sentiment analysis tool
   🏷️ 类型: local
   ✅ 已安装
```

## 🎨 用户体验

### 搜索体验
- **快速响应**: 本地技能毫秒级响应
- **智能排序**: 最相关的技能排在前面
- **丰富信息**: 显示类型、状态、大小等详细信息
- **去重处理**: 避免重复显示相同技能

### 管理体验
- **安全操作**: 卸载前自动备份
- **状态显示**: 清晰的安装状态指示
- **批量操作**: 支持批量更新和管理
- **错误处理**: 友好的错误提示和解决建议

### 推荐体验
- **智能推荐**: 基于对话上下文推荐
- **个性化**: 根据使用历史推荐
- **多样性**: 推荐不同类型的技能
- **可解释**: 显示推荐原因

## 🔧 技术实现

### 核心组件
1. **ClawHubUpgraded**: 主要的技能管理类
2. **搜索引擎**: 多源搜索和智能排序
3. **缓存系统**: 本地技能信息缓存
4. **推荐引擎**: 基于上下文的技能推荐

### 依赖管理
- **必需依赖**: Python 3.7+
- **可选依赖**: web-search, sentiment-analyzer
- **外部依赖**: npx (ClawHub CLI)

### 性能优化
- **缓存机制**: 避免重复扫描
- **并行搜索**: 多源并行搜索
- **智能排序**: 相关性优先排序
- **增量更新**: 只更新变化的技能

## 🚀 与原版对比

| 功能 | 原版ClawHub | 升级版ClawHub |
|------|-------------|---------------|
| 搜索范围 | 仅远程 | 本地+远程+网络 |
| 搜索速度 | 依赖网络 | 本地毫秒级响应 |
| 智能排序 | 基础排序 | 智能相关性排序 |
| 技能管理 | 基础安装 | 完整管理功能 |
| 推荐系统 | 无 | 智能上下文推荐 |
| 缓存机制 | 无 | 本地缓存优化 |
| 错误处理 | 基础 | 完善的错误处理 |
| 用户体验 | 命令行 | 友好的界面 |

## 🎯 使用场景

### 1. 技能发现
```
用户: "我需要一个能处理数据的技能"
系统: 推荐data-analyzer、data-scraper等技能
```

### 2. 技能管理
```
用户: "帮我安装web-scraper技能"
系统: 一键安装并验证功能
```

### 3. 技能更新
```
用户: "更新所有技能"
系统: 批量更新并报告结果
```

### 4. 技能查询
```
用户: "告诉我web-search技能的详细信息"
系统: 显示完整的技能信息
```

## 📈 未来规划

### 短期目标
- [ ] 添加技能评分系统
- [ ] 支持技能依赖关系分析
- [ ] 添加技能使用统计
- [ ] 支持技能版本管理

### 长期目标
- [ ] Web界面支持
- [ ] 技能自动测试
- [ ] 技能质量评估
- [ ] 社区技能推荐

## 🎉 总结

升级版ClawHub技能提供了：

1. ✅ **强大的搜索功能**: 多源搜索、智能排序、快速响应
2. ✅ **完整的技能管理**: 安装、卸载、更新、备份
3. ✅ **智能推荐系统**: 基于上下文的个性化推荐
4. ✅ **优秀的用户体验**: 友好的界面、丰富的信息、完善的错误处理
5. ✅ **高性能优化**: 缓存机制、并行搜索、智能排序

这个升级版技能将大大提升nanobot系统的技能发现和管理能力，让用户能够更轻松地找到和使用合适的技能！

---

**版本**: v2.0  
**更新时间**: 2026-03-11  
**作者**: 火娃 (nanobot)