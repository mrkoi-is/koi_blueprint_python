import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.dependencies import init_database, shutdown_database
from app.core.exception_handlers import app_error_handler, validation_error_handler
from app.core.exceptions import AppError
from app.core.logging import setup_logging

# 取消下行注释以启用 Prometheus 指标 / Uncomment to enable Prometheus metrics:
# from app.core.metrics import setup_metrics


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_database(app)
    yield
    shutdown_database(app)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

    @app.middleware("http")
    async def logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            trace_id=str(uuid.uuid4()),
            method=request.method,
            path=str(request.url.path),
        )
        return await call_next(request)

    # 启用 Prometheus 指标 / Enable Prometheus metrics
    # setup_metrics(app)

    api_prefix = "/api/v1"
    # 在此注册领域路由 / register domain routers here
    # app.include_router(example_router, prefix=api_prefix)
    _ = api_prefix

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
