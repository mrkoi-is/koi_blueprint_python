from contextlib import asynccontextmanager
import uuid

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.exception_handlers import app_error_handler, validation_error_handler
from app.core.exceptions import AppError
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup：此处管理需要异步初始化的长连接资源
    # engine = create_engine(str(settings.database_url), pool_size=5, max_overflow=10)
    # redis_client = redis.from_url(settings.redis_url)
    yield
    # Shutdown
    # engine.dispose()
    # redis_client.close()


def create_app() -> FastAPI:
    # 日志在进程启动时立即初始化，早于任何模块级日志调用
    setup_logging()

    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    @app.middleware("http")
    async def logging_middleware(request, call_next):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            trace_id=str(uuid.uuid4()),
            method=request.method,
            path=str(request.url.path),
        )
        return await call_next(request)

    api_prefix = "/api/v1"
    # 在此注册领域路由 / register domain routers here
    # app.include_router(example_router, prefix=api_prefix)
    _ = api_prefix

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
