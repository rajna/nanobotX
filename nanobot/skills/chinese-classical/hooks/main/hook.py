# -*- coding: utf-8 -*-
"""
Chinese to Classical Chinese Hook

策略：
1. 最近 N 条消息：保持原样
2. Token 阈值过滤：只压缩 > min_tokens 的消息
3. 技术内容检测：跳过代码/技术内容占比过高的消息
4. 概率触发：避免频繁使用
5. LLM 压缩：智能压缩旁白中文
6. 已压缩消息：跳过
"""

from __future__ import annotations

import re
import random
from typing import Any

# =============================================================================
# 配置
# =============================================================================

DEFAULT_SKIP_RECENT = 3
DEFAULT_MIN_LENGTH = 10
DEFAULT_MIN_TOKENS = 500          # 新增：最小 token 阈值
DEFAULT_TECH_RATIO = 0.3          # 新增：技术内容最大占比（30%）
DEFAULT_PROBABILITY = 0.5         # 新增：压缩触发概率（50%）
DEFAULT_LLM_MIN_LENGTH = 50
DEFAULT_LLM_MAX_LENGTH = 4000
COMPRESSION_THRESHOLD = 0.95


LLM_COMPRESS_PROMPT = """将以下现代中文转换为简洁的文言文。

规则：
1. 保持原意不变
2. 尽可能简洁
3. 保留代码、URL、数字不变
4. 只输出转换结果

现代中文：
{text}

文言文："""


# =============================================================================
# 替换规则
# =============================================================================

REPLACEMENT_RULES = [
    ("我想请你帮我", "请"),
    ("请你帮我", "请"),
    ("麻烦你帮我", "请"),
    ("能不能请你", "可否请"),
    ("能不能", "可否"),
    ("可以吗", "可乎"),
    ("分析一下", "析"),
    ("解释一下", "释"),
    ("说明一下", "述"),
    ("这个问题", "此问"),
    ("这个方案", "此策"),
    ("为什么", "何故"),
    ("怎么样", "如何"),
    ("这个", "此"),
    ("那个", "彼"),
    ("因为", "因"),
    ("所以", "故"),
    ("但是", "然"),
    ("而且", "且"),
    ("一下", ""),
    ("的话", ""),
]


# =============================================================================
# 保护机制
# =============================================================================

PROTECT_PATTERNS = [
    (re.compile(r'```[\s\S]*?```', re.MULTILINE), "CODE"),
    (re.compile(r'`[^`]+`'), "ICODE"),
    (re.compile(r'https?://[^\s<>"\'\{\}\|\\^\`\[\]]+'), "URL"),
    (re.compile(r'\b[A-Za-z]{2,}\b'), "EN"),
    (re.compile(r'\b\d+\.?\d*\b'), "NUM"),
]


def protect_content(text: str) -> tuple[str, dict[str, str]]:
    """保护代码、URL 等不被转换"""
    placeholders = {}
    counter = [0]
    
    def add_placeholder(match: re.Match, prefix: str) -> str:
        key = f"__{prefix}_{counter[0]}__"
        counter[0] += 1
        placeholders[key] = match.group(0)
        return key
    
    result = text
    for pattern, prefix in PROTECT_PATTERNS:
        result = pattern.sub(lambda m: add_placeholder(m, prefix), result)
    
    return result, placeholders


def restore_content(text: str, placeholders: dict[str, str]) -> str:
    """恢复被保护的内容"""
    result = text
    for key, value in placeholders.items():
        result = result.replace(key, value)
    return result


# =============================================================================
# Token 估算
# =============================================================================

def estimate_tokens(text: str) -> int:
    """
    估算 token 数量
    中文约 1.5 字符 = 1 token，英文约 4 字符 = 1 token
    """
    if not text:
        return 0
    
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    other_chars = len(text) - chinese_chars
    
    # 中文：1.5 字符 ≈ 1 token
    # 英文/其他：4 字符 ≈ 1 token
    tokens = int(chinese_chars / 1.5 + other_chars / 4)
    
    return max(1, tokens)


# =============================================================================
# 技术内容检测
# =============================================================================

def detect_tech_content_ratio(text: str) -> float:
    """
    检测技术内容占比
    返回 0-1 之间的值，表示技术内容占比
    """
    if not text:
        return 0.0
    
    total_len = len(text)
    if total_len == 0:
        return 0.0
    
    # 检测代码块
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    code_len = sum(len(cb) for cb in code_blocks)
    
    # 检测行内代码
    inline_code = re.findall(r'`[^`]+`', text)
    code_len += sum(len(ic) for ic in inline_code)
    
    # 检测 URL
    urls = re.findall(r'https?://[^\s<>"\'\{\}\|\\^\`\[\]]+', text)
    code_len += sum(len(u) for u in urls)
    
    # 检测英文单词（技术术语）
    english_words = re.findall(r'\b[A-Za-z]{3,}\b', text)
    code_len += sum(len(w) for w in english_words)
    
    return code_len / total_len


# =============================================================================
# 压缩方法
# =============================================================================

def compress_by_rules(text: str) -> str:
    """规则压缩（快速）"""
    if not text or len(text) < DEFAULT_MIN_LENGTH:
        return text
    
    protected, placeholders = protect_content(text)
    
    result = protected
    for old, new in REPLACEMENT_RULES:
        result = result.replace(old, new)
    
    result = re.sub(r'\s+', '', result)
    result = restore_content(result, placeholders)
    
    # 如果压缩效果不明显，返回原文
    if len(result) >= len(text) * COMPRESSION_THRESHOLD:
        return text
    
    return result


def get_response_content(response: Any) -> str | None:
    """从响应中获取内容，支持多种格式"""
    # 标准 content
    if hasattr(response, 'content') and response.content:
        return response.content
    
    # 智谱等推理模型的 reasoning_content
    if hasattr(response, 'reasoning_content') and response.reasoning_content:
        return response.reasoning_content
    
    # 字典格式
    if isinstance(response, dict):
        if response.get('content'):
            return response['content']
        if response.get('reasoning_content'):
            return response['reasoning_content']
    
    return None


async def compress_by_llm(
    text: str,
    provider: Any,
    model: str,
    min_length: int = DEFAULT_LLM_MIN_LENGTH,
    max_length: int = DEFAULT_LLM_MAX_LENGTH,
) -> str:
    """LLM 压缩（智能，更高压缩率）"""
    from loguru import logger
    
    if not text or len(text) < min_length:
        return text
    
    if len(text) > max_length:
        return await compress_long_text_by_llm(text, provider, model, max_length)
    
    try:
        prompt = LLM_COMPRESS_PROMPT.format(text=text)
        
        response = await provider.chat(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=min(len(text), 500),
            temperature=0.3,
        )
        
        result = get_response_content(response)
        
        if result:
            result = result.strip()
            if len(result) < len(text) * 0.95:
                logger.info(f"LLM 压缩: {len(text)} -> {len(result)}")
                return result
            
    except Exception as e:
        logger.warning(f"LLM 压缩失败: {e}")
    
    # LLM 失败时返回原文
    return text


async def compress_long_text_by_llm(
    text: str,
    provider: Any,
    model: str,
    chunk_size: int,
) -> str:
    """分段处理长文本"""
    sentences = re.split(r'([。！？\n])', text)
    chunks = []
    current = ""
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        if i + 1 < len(sentences):
            sentence += sentences[i + 1]
        
        if len(current) + len(sentence) > chunk_size:
            if current:
                chunks.append(current)
            current = sentence
        else:
            current += sentence
    
    if current:
        chunks.append(current)
    
    results = []
    for chunk in chunks:
        result = await compress_by_llm(chunk, provider, model)
        results.append(result)
    
    return "".join(results)


# =============================================================================
# 消息处理
# =============================================================================

def should_skip_message(msg: dict) -> bool:
    """判断是否跳过消息"""
    # 跳过工具调用
    if msg.get("tool_calls") or msg.get("tool_call_id"):
        return True
    
    # 跳过系统消息
    if msg.get("role") == "system":
        return True
    
    # 跳过已压缩的消息
    if msg.get("_compressed"):
        return True
    
    return False


def is_already_compressed(msg: dict) -> bool:
    """检查消息是否已压缩"""
    return msg.get("_compressed", False)


async def process_message(
    msg: dict,
    index: int,
    total: int,
    options: dict,
    provider: Any,
    model: str,
) -> tuple[dict, int, str]:
    """
    处理单条消息
    
    Returns:
        (msg, saved, skip_reason)
    """
    skip_recent = options.get("skip_recent", DEFAULT_SKIP_RECENT)
    enable_llm = options.get("enable_llm", True)
    min_length = options.get("min_length", DEFAULT_MIN_LENGTH)
    min_tokens = options.get("min_tokens", DEFAULT_MIN_TOKENS)      # 新增
    tech_ratio = options.get("tech_ratio", DEFAULT_TECH_RATIO)      # 新增
    probability = options.get("probability", DEFAULT_PROBABILITY)   # 新增
    llm_min_length = options.get("llm_min_length", DEFAULT_LLM_MIN_LENGTH)
    llm_max_length = options.get("llm_max_length", DEFAULT_LLM_MAX_LENGTH)
    
    # 最近的消息不处理
    if index >= total - skip_recent:
        return msg, 0, "recent"
    
    # 跳过特殊消息
    if should_skip_message(msg):
        return msg, 0, "special"
    
    content = msg.get("content")
    if not content or not isinstance(content, str):
        return msg, 0, "no_content"
    
    if len(content) < min_length:
        return msg, 0, "too_short"
    
    # 新增：Token 阈值检查
    tokens = estimate_tokens(content)
    if tokens < min_tokens:
        return msg, 0, f"below_token_threshold({tokens}<{min_tokens})"
    
    # 新增：技术内容检测
    tech_content_ratio = detect_tech_content_ratio(content)
    if tech_content_ratio > tech_ratio:
        return msg, 0, f"too_much_tech_content({tech_content_ratio:.1%}>{tech_ratio:.1%})"
    
    # 新增：概率触发
    if random.random() > probability:
        return msg, 0, f"probability_skip({random.random():.2f}>{probability})"
    
    original_len = len(content)
    
    # 只使用 LLM 压缩
    if enable_llm and provider and model:
        compressed = await compress_by_llm(
            content, provider, model,
            min_length=llm_min_length,
            max_length=llm_max_length,
        )
    else:
        compressed = content
    
    if compressed != content:
        saved = original_len - len(compressed)
        # 标记为已压缩
        return {**msg, "content": compressed, "_compressed": True}, saved, "compressed"
    
    return msg, 0, "no_compression"


# =============================================================================
# Hook 入口
# =============================================================================

async def execute(context: dict[str, Any]) -> dict[str, Any]:
    """Hook 入口函数"""
    from loguru import logger
    
    messages = context.get("messages", [])
    if not messages:
        return context
    
    options = context.get("_options", {})
    provider = context.get("provider")
    model = context.get("model")
    enable_llm = options.get("enable_llm", True)
    
    # 统计已压缩消息
    already_compressed = sum(1 for m in messages if is_already_compressed(m))
    
    # 新增：读取配置
    min_tokens = options.get("min_tokens", DEFAULT_MIN_TOKENS)
    tech_ratio = options.get("tech_ratio", DEFAULT_TECH_RATIO)
    probability = options.get("probability", DEFAULT_PROBABILITY)
    
    logger.info(
        "Hook 'chinese-classical': {} msgs ({} compressed), LLM: {}, min_tokens: {}, tech_ratio: {:.0%}, probability: {:.0%}",
        len(messages), already_compressed, enable_llm and provider is not None,
        min_tokens, tech_ratio, probability
    )
    
    processed_messages = []
    total = len(messages)
    total_saved = 0
    compressed_count = 0
    skip_reasons = {}
    
    for i, msg in enumerate(messages):
        # 跳过已压缩的
        if is_already_compressed(msg):
            processed_messages.append(msg)
            continue
        
        processed_msg, saved, skip_reason = await process_message(
            msg, i, total, options, provider, model
        )
        processed_messages.append(processed_msg)
        total_saved += saved
        
        # 统计跳过原因
        if skip_reason and skip_reason != "compressed":
            skip_reasons[skip_reason] = skip_reasons.get(skip_reason, 0) + 1
        
        if saved > 0:
            compressed_count += 1
    
    if total_saved > 0 or skip_reasons:
        original_total = sum(
            len(m.get("content", ""))
            for m in messages
            if isinstance(m.get("content"), str)
        )
        rate = total_saved / original_total * 100 if original_total > 0 else 0
        
        logger.info(
            "Hook 'chinese-classical': compressed {}, saved {} chars ({:.1f}%), skips: {}",
            compressed_count, total_saved, rate,
            ", ".join([f"{k}={v}" for k, v in skip_reasons.items()])
        )
    
    return {**context, "messages": processed_messages}
