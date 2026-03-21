---
name: add-observability
description: Add observability infrastructure to a Koi-standard Python service. Use when wiring Prometheus metrics, OpenTelemetry tracing, OTLP or Jaeger export, local observability compose assets, and verifying logs/metrics/traces coverage for production services.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 接入 `Prometheus` 指标、`/metrics` 暴露与基础监控
- 接入 `OpenTelemetry` tracing、OTLP / Jaeger 导出
- 为本地联调补 `Prometheus` / `Grafana` / `Jaeger` 资产
- 审核日志、指标、链路追踪覆盖是否达到上线要求

## Workflow

1. Read `docs/architecture.md` 中与日志、可观测性、运行时配置相关的章节。
2. Inspect the target project's:
   - `app/main.py`
   - `app/config.py`
   - `app/core/logging.py`
   - `app/core/metrics.py`
   - `app/core/` tracing-related files
   - Docker / compose assets
   - tests for `/health` and `/metrics`
3. Run `scripts/inspect_observability_surface.py <target-root>` to collect current observability signals.
4. Use `references/metrics-checklist.md` to decide metrics exposure, labels, and endpoint policy.
5. Use `references/tracing-checklist.md` to decide trace provider, exporter, sampling, and propagation.
6. If the project needs a local observability stack, start from `assets/docker-compose.observability.template.yml` and `assets/prometheus.yml`.
7. Keep logs, metrics, and traces aligned on service name, environment, and request correlation identifiers.

## Observability Principles

- 指标先解决“是否可测量”，再补面板；不要先堆 Grafana 截图。
- 链路追踪只在确有价值时启用，采样率与 exporter 必须可配置。
- `/metrics`、`/health`、`/ready` 的职责边界要清晰，不要混用。
- 日志、指标、trace 的服务名与环境标签必须统一，否则后期排障成本会很高。

Load `references/metrics-checklist.md` and `references/tracing-checklist.md` as needed.
