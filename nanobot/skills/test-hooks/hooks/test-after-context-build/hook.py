async def execute(context):
    """Hook 入口函数"""
    from loguru import logger
    
    # 使用 logger 而不是 print
    # logger.info("===== TEST HOOK CALLED =====")
    messages = context.get('messages', [])
    logger.info(messages)
    logger.info(f"test after_context_build Messages count: {len(context.get('messages', []))}")
    return context
