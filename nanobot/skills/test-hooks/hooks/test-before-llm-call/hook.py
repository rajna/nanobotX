"""before Context Build Hook - 统计上下文长度"""

from __future__ import annotations
from typing import Any


async def execute(context: dict[str, Any]) -> dict[str, Any]:
    """Hook 入口函数 - 统计最长的 context 内容"""
    from loguru import logger
    
    messages = context.get('messages', [])
    if not messages:
        return context
    
    # 统计总长度
    total_length = 0
    message_stats = []
    
    for i, msg in enumerate(messages):
        content = ""
        if isinstance(msg, dict):
            content = msg.get('content', '')
        elif hasattr(msg, 'content'):
            content = getattr(msg, 'content', '')
        else:
            content = str(msg)
        
        content_len = len(content)
        total_length += content_len
        
        # 获取角色
        role = msg.get('role', 'unknown') if isinstance(msg, dict) else 'unknown'
        
        # 截取前100字符作为预览
        preview = content[:100] + "..." if len(content) > 100 else content
        preview = preview.replace('\n', ' ')[:80]  # 单行显示
        
        message_stats.append({
            'index': i,
            'role': role,
            'length': content_len,
            'preview': preview
        })
    
    # 按长度排序，找出最长的5条
    sorted_stats = sorted(message_stats, key=lambda x: x['length'], reverse=True)
    top5 = sorted_stats[:5]
    
    # 记录统计信息
    logger.info(f"📊 上下文统计: 总消息数={len(messages)}, 总字符数={total_length}")
    
    # if top5:
    #     logger.info(f"📈 最长的 {len(top5)} 条消息:")
    #     for stat in top5:
    #         logger.info(f"  [{stat['index']:3d}] {stat['role']:8s} {stat['length']:6d}字符 | {stat['preview']}")
    
    # 检查是否接近上下文限制（假设限制为 128k）
    WARNING_THRESHOLD = 100000  # 100k 字符警告
    if total_length > WARNING_THRESHOLD:
        logger.warning(f"⚠️ 上下文过长: {total_length} 字符，建议清理历史消息")
    
    return context
