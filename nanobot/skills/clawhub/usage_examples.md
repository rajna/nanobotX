# ClawHub Upgraded 使用示例

## 🎯 快速开始

### 1. 基本搜索

```bash
# 搜索所有相关技能
python clawhub.py search "web scraping" 10 all

# 只搜索本地技能
python clawhub.py search "data analysis" 5 local

# 只搜索远程技能
python clawhub.py search "machine learning" 3 remote
```

### 2. 技能管理

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

### 3. 智能推荐

```bash
# 基于上下文推荐
python clawhub.py recommend "I need data analysis"

# 通用推荐
python clawhub.py recommend
```

### 4. 技能更新

```bash
# 更新所有技能
python clawhub.py update

# 更新指定技能
python clawhub.py update web-scraper data-analyzer
```

## 📋 实际使用场景

### 场景1: 发现新技能

```
用户: "我需要一个能处理网页数据的技能"
系统: 
🔍 搜索结果: 'web data'
============================================================
1. web-scraper
   📝 Web scraping and data extraction tool
   🏷️ 类型: remote
   📦 可安装
   ⭐ 相关度: 8

2. web-search
   📝 Advanced web search and content extraction
   🏷️ 类型: local
   ✅ 已安装
   ⭐ 相关度: 6

3. data-processor
   📝 Data processing and analysis tool
   🏷️ 类型: remote
   📦 可安装
   ⭐ 相关度: 7
```

### 场景2: 管理现有技能

```
用户: "帮我管理一下技能"
系统:
📋 技能列表 (类型: all)
============================================================
📦 web-search
   📝 Advanced web search and content extraction
   🏷️ 类型: local
   ✅ 状态: 可用
   📁 大小: 2.45 MB

📦 stock-query
   📝 A-share stock information query tool
   🏷️ 类型: local
   ✅ 状态: 可用
   📁 大小: 1.82 MB

📦 sentiment-analyzer
   📝 Advanced sentiment analysis tool
   🏷️ 类型: local
   ✅ 状态: 可用
   📁 大小: 3.14 MB
```

### 场景3: 智能推荐

```
用户: "我需要分析股票数据"
系统:
🎯 技能推荐 (基于: 'I need stock data analysis')
============================================================
1. stock-query
   📝 A-share stock information query tool
   🏷️ 类型: local
   ✅ 已安装

2. data-analyzer
   📝 Advanced data analysis and visualization tool
   🏷️ 类型: remote
   📦 可安装

3. financial-modeler
   📝 Financial modeling and analysis tool
   🏷️ 类型: remote
   📦 可安装
```

### 场景4: 技能详细信息

```
用户: "告诉我web-search技能的详细信息"
系统:
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
```

## 🔧 高级用法

### 1. 批量操作

```bash
# 批量更新技能
python clawhub.py update web-search stock-query sentiment-analyzer

# 批量搜索多个关键词
python clawhub.py search "web scraping" 5 all
python clawhub.py search "data analysis" 5 all
python clawhub.py search "machine learning" 5 all
```

### 2. 自定义搜索

```bash
# 限制搜索结果数量
python clawhub.py search "AI" 3 all

# 按类型搜索
python clawhub.py search "analysis" 10 local
python clawhub.py search "learning" 5 remote
```

### 3. 技能健康检查

```bash
# 检查所有技能状态
python clawhub.py list all

# 检查特定技能
python clawhub.py info web-search
python clawhub.py info stock-query
```

## 🎨 输出格式说明

### 搜索结果格式
```
🔍 搜索结果: '关键词'
============================================================
1. 技能名称
   📝 技能描述
   🏷️ 类型: local/remote/web
   ✅/📦/❌ 状态: 已安装/可安装/不可用
   ⭐ 相关度: 分数
```

### 技能列表格式
```
📋 技能列表 (类型: all/local/remote)
============================================================
📦 技能名称
   📝 技能描述
   🏷️ 类型: local/remote/web
   ✅ 状态: 可用/不可用
   📁 大小: MB
```

### 技能信息格式
```
📋 技能信息: 技能名称
============================================================
📝 技能描述
🏷️ 类型: local/remote/web
📍 路径: 完整路径
✅ 状态: 可用/不可用
📅 安装时间: YYYY-MM-DDTHH:MM:SS
📁 大小: MB
📄 文件数量: 数量
📁 主要文件:
   - 文件1
   - 文件2
   ...
```

### 推荐结果格式
```
🎯 技能推荐 (基于: '上下文')
============================================================
1. 技能名称
   📝 技能描述
   🏷️ 类型: local/remote/web
   ✅/📦 状态: 已安装/可安装
```

## 🚀 性能优化

### 1. 使用本地缓存
- 本地技能信息已缓存，搜索速度极快
- 避免重复扫描目录

### 2. 智能搜索
- 相关性排序确保最相关的结果在前
- 去重处理避免重复显示

### 3. 批量操作
- 支持批量更新和管理
- 减少重复操作

## ⚠️ 注意事项

### 1. 网络依赖
- 远程技能搜索需要网络连接
- 建议在网络良好时使用

### 2. 权限要求
- 安装技能需要写入技能目录的权限
- 卸载技能需要删除文件的权限

### 3. 备份机制
- 卸载技能时会自动备份
- 备份文件保存在技能目录中

### 4. 缓存更新
- 本地技能缓存会定期更新
- 修改技能后需要重新扫描

## 🎯 最佳实践

### 1. 搜索技巧
- 使用具体的关键词获得更好的结果
- 结合多个关键词进行搜索
- 限制结果数量以提高效率

### 2. 技能管理
- 定期更新技能以获得最新功能
- 使用批量操作提高效率
- 定期检查技能状态

### 3. 推荐使用
- 基于当前需求使用推荐功能
- 结合搜索和推荐发现新技能
- 关注推荐的相关性分数

## 📞 故障排除

### 1. 搜索无结果
- 检查网络连接（远程搜索）
- 尝试不同的关键词
- 检查技能目录权限

### 2. 安装失败
- 检查技能名称是否正确
- 确保有足够的磁盘空间
- 检查网络连接

### 3. 卸载失败
- 检查文件权限
- 确保技能没有被其他程序使用
- 查看错误日志

### 4. 推荐不准确
- 提供更具体的上下文
- 尝试不同的描述方式
- 结合搜索功能手动查找

---

**版本**: v2.0  
**更新时间**: 2026-03-11  
**作者**: 火娃 (nanobot)