---
name: add-observability
description: Add observability infrastructure (Metrics, Tracing) to a Koi-standard Python service. Use when integrating Prometheus metrics, OpenTelemetry tracing, or Grafana dashboards for production monitoring.
---

> 适配 `docs/architecture.md` v4.0

## 三大支柱 (Three Pillars)

| 支柱 | 工具 | 状态 |
|---|---|---|
| **Logs** | structlog (已内置) | ✅ 默认包含 |
| **Metrics** | prometheus-fastapi-instrumentator | 需安装 |
| **Traces** | opentelemetry-api + jaeger/zipkin | 需安装 |

## Workflow: Metrics (Prometheus)

1. 安装: `uv add prometheus-fastapi-instrumentator`
2. skeleton 已包含 `app/core/metrics.py`，在 `create_app()` 中调用:
   ```python
   from app.core.metrics import setup_metrics
   setup_metrics(app)
   ```
3. 访问 `/metrics` 查看 Prometheus 指标
4. 可选: 在 `docker-compose.yml` 中添加 Prometheus + Grafana

## Workflow: Tracing (OpenTelemetry)

1. 安装:
   ```bash
   uv add opentelemetry-api opentelemetry-sdk
   uv add opentelemetry-instrumentation-fastapi
   uv add opentelemetry-exporter-otlp  # 或 jaeger
   ```
2. 在 `app/core/tracing.py` 中配置:
   ```python
   from opentelemetry import trace
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

   def setup_tracing(app):
       provider = TracerProvider()
       trace.set_tracer_provider(provider)
       FastAPIInstrumentor.instrument_app(app)
   ```
3. 在 `create_app()` 中调用 `setup_tracing(app)`

## docker-compose 扩展

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports: ["16686:16686", "4317:4317"]
```
