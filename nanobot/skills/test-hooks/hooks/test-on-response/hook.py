async def execute(context):
    """Hook 入口函数"""
    from loguru import logger
    
    # 使用 logger 而不是 print
    # logger.info("===== TEST HOOK CALLED =====")
    logger.info(f"on_response Messages count: {len(context.get('messages', []))}")
    return context
