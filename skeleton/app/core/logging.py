# 结构化日志初始化 — dev/prod 双模式输出
import logging

import structlog

from app.config import settings


def setup_logging() -> None:
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,  # 自动注入 trace_id, user_id 等
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.debug:
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # 桥接标准库 logging：第三方库（uvicorn、sqlalchemy 等）通过
    # logging.getLogger() 输出的日志也会流经 structlog 处理链，
    # 确保整个进程日志格式统一。
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
        ],
        force=True,
    )

    # 将标准库日志处理器替换为 structlog 格式化器
    for handler in logging.root.handlers:
        handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=renderer,
                foreign_pre_chain=shared_processors,
            )
        )
