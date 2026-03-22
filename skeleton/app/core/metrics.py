"""可观测性: Prometheus 指标收集

通过 prometheus-fastapi-instrumentator 自动暴露 HTTP 请求指标到 /metrics 端点。

用法:
    # 在 app/main.py 的 create_app() 中:
    from app.core.metrics import setup_metrics
    setup_metrics(app)

依赖:
    uv add prometheus-fastapi-instrumentator
"""

from fastapi import FastAPI


def setup_metrics(app: FastAPI) -> None:
    """配置 Prometheus 指标收集。

    自动记录:
    - 请求总数 (按 method, path, status)
    - 请求延迟直方图
    - 活跃请求数
    - 请求/响应体大小
    """
    try:
        from prometheus_fastapi_instrumentator import Instrumentator

        Instrumentator(
            should_group_status_codes=True,
            should_ignore_untemplated=True,
            should_instrument_requests_inprogress=True,
            excluded_handlers=["/health", "/metrics"],
            inprogress_name="http_requests_inprogress",
            inprogress_labels=True,
        ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
    except ImportError:
        import structlog

        logger = structlog.get_logger()
        logger.warning(
            "prometheus-fastapi-instrumentator 未安装，跳过 Metrics 配置。"
            "运行 `uv add prometheus-fastapi-instrumentator` 启用。"
        )
