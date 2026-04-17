"""
Before Context Build Hook - 基于用户反馈的任务评分

在构建LLM context之前：
1. 分析当前用户消息，判断上一个任务的成功/失败
2. 根据用户反馈调整评分
3. 保存并优化上一个任务
4. 记录新任务开始时间
"""
from __future__ import annotations

from typing import Any
from pathlib import Path
import time


# 全局变量
_optimizer = None
_current_task_start_time = None
_current_task_description = None


def get_optimizer(options: dict) -> Any:
    """获取或创建优化器实例"""
    global _optimizer

    if _optimizer is not None:
        return _optimizer

    import sys
    import os

    # 添加 scripts 目录到路径
    hook_dir = Path(__file__).parent
    scripts_dir = hook_dir.parent.parent / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from skill_chain_optimizer import SkillChainOptimizer

    # 获取配置
    storage_path = options.get(
        "storage_path",
        str(Path.home() / ".nanobot" / "data" / "skill-chains")
    )
    similarity_threshold = options.get("similarity_threshold", 0.35)
    max_chains_per_task = options.get("max_chains_per_task", 5)

    _optimizer = SkillChainOptimizer(
        storage_path=storage_path,
        similarity_threshold=similarity_threshold,
        max_chains_per_task=max_chains_per_task,
    )
    _optimizer.initialize()

    return _optimizer


async def abstract_task_description_with_ai(
    message: str,
    provider: Any,
    model: str
) -> str:
    """
    使用AI将具体的任务描述抽象化为通用类别

    Args:
        message: 用户原始消息
        provider: LLM provider
        model: 模型名称

    Returns:
        抽象后的任务描述
    """
    if not message:
        return "Unknown task"

    # 构建提示词
    prompt = f"""你是一个任务分类助手。请将用户的任务描述抽象化为一个通用的类别名称。

用户任务: {message}

请返回JSON格式的结果，包含以下字段：
- category: 任务类别名称（简洁的中文短语，不超过10个字）



只返回JSON，不要有其他内容。"""

    try:
        response = await provider.chat(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=100,
            temperature=0.1,
        )

        if response.content:
            import json
            result = json.loads(response.content)
            category = result.get("category", "其他")
            return category
    except Exception as e:
        # AI抽象失败，回退到规则匹配
        pass

    return abstract_task_description(message)


def abstract_task_description(message: str) -> str:
    """
    将具体的任务描述抽象化为通用类别（规则匹配版本）

    Args:
        message: 用户原始消息

    Returns:
        抽象后的任务描述
    """
    if not message:
        return "Unknown task"

    message_lower = message.lower()

    # 任务类型映射规则
    task_patterns = [
        # 股票分析类
        (r"分析.*股票|分析.*\d{6}|分析.*[a-z]{2}\.\d{6}", "分析股票"),
        (r"股票.*分析|查询.*股票|获取.*股票", "分析股票"),
        (r"涨跌|行情|走势|K线|均线|成交量", "分析股票"),

        # 天气查询类
        (r"天气|气温|温度|下雨|下雪|刮风", "查询天气"),

        # 搜索类
        (r"搜索|查找|找一下|百度|google", "搜索信息"),

        # 总结类
        (r"总结|摘要|概括|提取要点", "总结内容"),

        # 翻译类
        (r"翻译|translate|英文|中文", "翻译文本"),

        # 代码类
        (r"代码|编程|写.*函数|实现.*功能", "编写代码"),

        # 默认：使用原始消息的前50个字符
    ]

    import re
    for pattern, abstract_desc in task_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return abstract_desc

    # 如果没有匹配到，返回原始消息的摘要
    return message[:50] + "..." if len(message) > 50 else message


async def analyze_user_feedback_with_ai(
    message: str,
    provider: Any,
    model: str
) -> tuple[bool, float]:
    """
    使用AI分析用户反馈，判断任务成功/失败并返回评分调整系数

    Args:
        message: 用户反馈消息
        provider: LLM provider
        model: 模型名称

    Returns:
        (task_completed, score_multiplier)
    """
    if not message:
        return True, 1.0

    # 构建提示词
    prompt = f"""你是一个任务评价助手。请根据用户的反馈，判断上一个任务是否成功完成，并给出评分调整系数。

用户反馈: {message}

请返回JSON格式的结果，包含以下字段：
- task_completed: 布尔值，表示任务是否完成（true/false）
- score_multiplier: 浮点数，表示评分调整系数（范围：0.5-1.5）
  - 1.5: 非常满意，任务完成得很好
  - 1.2: 满意，任务完成得不错
  - 1.0: 一般，任务基本完成
  - 0.8: 不太满意，任务有些问题
  - 0.5: 不满意，任务失败

只返回JSON，不要有其他内容。"""

    try:
        response = await provider.chat(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=200,
            temperature=0.1,
        )

        if response.content:
            import json
            result = json.loads(response.content)
            task_completed = result.get("task_completed", True)
            score_multiplier = float(result.get("score_multiplier", 1.0))
            # 限制范围
            score_multiplier = max(0.5, min(1.5, score_multiplier))
            return task_completed, score_multiplier
    except Exception as e:
        # AI评价失败，回退到规则匹配
        pass

    return True, 1.0


async def analyze_user_feedback_sentiment(
    message: str,
    provider: Any,
    model: str
) -> tuple[bool, float]:
    """
    使用AI情感分析判断用户反馈是正面还是负面

    Args:
        message: 用户反馈消息
        provider: LLM provider
        model: 模型名称

    Returns:
        (is_positive, score_multiplier)
        - is_positive: True=正面反馈, False=负面反馈
        - score_multiplier: 评分调整系数（1.2=正面, 0.5=负面）
    """
    if not message:
        return True, 1.0

    # 构建提示词
    prompt = f"""你是一个情感分析助手。请分析用户的反馈，判断是正面还是负面。

用户反馈: {message}

请返回JSON格式的结果，包含以下字段：
- is_positive: 布尔值，表示反馈是否正面（true/false）
- confidence: 浮点数，表示置信度（0.0-1.0）

只返回JSON，不要有其他内容。"""

    try:
        response = await provider.chat(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=200,
            temperature=0.1,
        )

        if response.content:
            import json
            result = json.loads(response.content)
            is_positive = result.get("is_positive", True)
            confidence = float(result.get("confidence", 0.5))

            # 根据情感判断返回评分系数
            if is_positive:
                return True, 1.2  # 正面反馈，评分提升20%
            else:
                return False, 0.5  # 负面反馈，评分减半
    except Exception as e:
        # AI情感分析失败，回退到规则匹配
        pass

    return True, 1.0


def analyze_user_feedback(message: str) -> tuple[bool, float]:
    """
    分析用户反馈，判断任务成功/失败并返回评分调整系数（规则匹配版本）

    Returns:
        (task_completed, score_multiplier)
    """
    if not message:
        return True, 1.0

    message_lower = message.lower()

    # 正面反馈关键词
    positive_keywords = [
        "好", "很好", "不错", "太棒了", "完美", "正确", "对", "是的",
        "谢谢", "感谢", "解决了", "成功", "可以", "行", "ok", "yes",
        "good", "great", "perfect", "correct", "thanks", "solved"
    ]

    # 负面反馈关键词
    negative_keywords = [
        "不对", "错误", "错了", "不行", "失败", "重试", "重新",
        "不是", "不对劲", "有问题", "错误", "error", "wrong", "no",
        "retry", "fail", "failed", "incorrect"
    ]

    # 检查负面反馈
    for keyword in negative_keywords:
        if keyword in message_lower:
            return False, 0.5  # 任务失败，评分减半

    # 检查正面反馈
    for keyword in positive_keywords:
        if keyword in message_lower:
            return True, 1.2  # 任务成功，评分提升20%

    # 默认：任务完成，评分不变
    return True, 1.0


async def execute(context: dict[str, Any]) -> dict[str, Any]:
    """Hook 入口函数"""
    from loguru import logger

    global _current_task_start_time, _current_task_description

    options = context.get("_options", {})

    # 从 context 中获取当前用户消息
    # 优先使用 current_message，如果没有则从 history 中获取
    current_message = context.get("current_message", "")
    if not current_message:
        history = context.get("history", [])
        for msg in reversed(history):
            if msg.get("role") == "user":
                current_message = msg.get("content", "")

    # 获取优化器
    optimizer = get_optimizer(options)

    # ============= 1. 结束上一个任务（基于用户反馈） =============
    if _current_task_start_time is not None and _current_task_description is not None:
        elapsed_time = time.time() - _current_task_start_time

        # 分析用户反馈
        # 优先使用AI情感分析，如果失败则回退到规则匹配
        provider = context.get("provider")
        model = context.get("model")

        if provider and model:
            try:
                # 使用AI情感分析判断正面/负面
                is_positive, score_multiplier = await analyze_user_feedback_sentiment(
                    current_message, provider, model
                )
                task_completed = is_positive  # 正面=完成，负面=未完成
                logger.debug(
                    "Hook 'skill-chain-optimizer': AI情感分析 - 正面: {}, 系数: {:.2f}",
                    is_positive, score_multiplier
                )
            except Exception as e:
                logger.debug(f"Hook 'skill-chain-optimizer': AI情感分析失败，回退到规则匹配: {e}")
                task_completed, score_multiplier = analyze_user_feedback(current_message)
        else:
            task_completed, score_multiplier = analyze_user_feedback(current_message)

        try:
            # 保存并优化上一个任务
            result = optimizer.save_and_optimize_chain(
                task_description=_current_task_description,
                task_completed=task_completed,
            )

            if result.get("saved"):
                skill_chain = result.get("skillChain", [])
                base_score = result.get("score", 0)

                # 根据用户反馈调整评分
                final_score = int(base_score * score_multiplier)
                final_score = max(0, min(100, final_score))  # 限制在0-100

                logger.info(
                    "Hook 'skill-chain-optimizer': 任务完成 [{}] 耗时: {:.1f}s 基础分: {} 反馈系数: {:.1f} 最终分: {}/100",
                    ", ".join(skill_chain),
                    elapsed_time,
                    base_score,
                    score_multiplier,
                    final_score
                )

                if result.get("isBestChain"):
                    logger.info("Hook 'skill-chain-optimizer': 🏆 这是目前最佳方案！")
            else:
                # 只在非"没有记录到skill调用"的情况下记录 debug
                reason = result.get("reason", "unknown")
                if "没有记录到skill调用" not in reason:
                    logger.debug(
                        "Hook 'skill-chain-optimizer': 未保存链 ({})",
                        reason
                    )
        except Exception as e:
            logger.error(f"Hook 'skill-chain-optimizer' end task failed: {e}")

    # ============= 2. 记录新任务开始 =============
    _current_task_start_time = time.time()

    # 使用AI抽象任务描述
    provider = context.get("provider")
    model = context.get("model")

    if provider and model:
        try:
            _current_task_description = await abstract_task_description_with_ai(
                current_message, provider, model
            )
            logger.debug(
                "Hook 'skill-chain-optimizer': AI抽象任务: {} (原始: {})",
                _current_task_description,
                current_message[:50] + "..." if len(current_message) > 50 else current_message
            )
        except Exception as e:
            logger.debug(f"Hook 'skill-chain-optimizer': AI抽象失败，回退到规则匹配: {e}")
            _current_task_description = abstract_task_description(current_message)
    else:
        _current_task_description = abstract_task_description(current_message)

    # 保存优化器实例供其他 hook 使用
    context["_optimizer"] = optimizer
    context["_current_task_start_time"] = _current_task_start_time
    context["_current_task_description"] = _current_task_description

    return context
