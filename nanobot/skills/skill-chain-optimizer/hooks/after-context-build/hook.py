"""
After Context Build Hook - 推荐最佳 skill chain

在构建上下文之后：
1. 获取用户消息
2. 查找相似任务
3. 推荐最佳 skill chain
"""
from __future__ import annotations

from typing import Any


async def execute(context: dict[str, Any]) -> dict[str, Any]:
    """Hook 入口函数"""
    from loguru import logger
    
    # 获取优化器实例
    optimizer = context.get("_optimizer")
    if not optimizer:
        return context
    
    # 获取任务描述
    task_description = context.get("_current_task_description")
    if not task_description:
        return context
    
    try:
        # 推荐最佳链
        recommendation = optimizer.recommend_chain_for_task(task_description)
        
        if recommendation.get("recommended"):
            skill_chain = recommendation.get("skillChain", [])
            confidence = recommendation.get("confidence", 0)
            score = recommendation.get("historicalScore", 0)
            
            logger.info(
                "Hook 'skill-chain-optimizer': 推荐链 [{}] (置信度: {:.0%}, 评分: {})",
                ", ".join(skill_chain),
                confidence,
                score
            )
            
            # 将推荐注入上下文
            context["_skill_chain_recommendation"] = {
                "recommended": True,
                "skillChain": skill_chain,
                "confidence": confidence,
                "historicalScore": score,
                "taskId": recommendation.get("taskId"),
            }
        else:
            logger.debug("Hook 'skill-chain-optimizer': 无历史推荐")
            context["_skill_chain_recommendation"] = {
                "recommended": False,
            }
        
    except Exception as e:
        logger.error(f"Hook 'skill-chain-optimizer' recommend failed: {e}")
    
    return context
