---
name: add-background-task
description: Add background task infrastructure to a Koi-standard Python service. Use when choosing between FastAPI BackgroundTasks, ARQ, or Celery, wiring workers and queues, defining retry/idempotency strategy, and testing asynchronous job flows.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 接入 `FastAPI BackgroundTasks`、`ARQ` 或 `Celery`
- 为邮件发送、报表导出、数据同步、定时任务选择后台执行方案
- 设计 task payload、重试策略、worker 部署方式
- 审核当前后台任务边界、可观测性与测试覆盖是否合理

## Workflow

1. Read `docs/architecture.md` 中与工具链、异步边界、日志、配置相关的章节。
2. Inspect the target project's:
   - `app/main.py`
   - `app/config.py`
   - `app/core/`
   - `app/domain/`
   - Docker / compose assets
   - tests for task-producing flows
3. Run `scripts/inspect_background_task_surface.py <target-root>` to inspect current queue, worker, and compose signals.
4. Use `references/strategy-guide.md` to choose `BackgroundTasks`、`ARQ` 或 `Celery`。
5. If the task is in-process and lightweight, load `references/fastapi-backgroundtasks-patterns.md`.
6. If the task needs persistence, retries, delayed execution, or worker isolation, load `references/queue-worker-patterns.md`.
7. Keep enqueue logic near router/service boundaries, and keep worker code free of HTTP-specific concerns.
8. Add or update tests for enqueue behavior, retry semantics, and failure handling when the queue becomes part of the architecture.

## Background Task Principles

- 轻量、短时、允许随请求进程一起结束的任务，优先 `BackgroundTasks`。
- 需要重试、延迟执行、独立扩缩容或高可靠队列时，再选 `ARQ` / `Celery`。
- Task payload 优先传递标识符或纯数据，不直接传 ORM 实体、Session 或 Request 对象。
- 后台任务必须考虑幂等性、超时、日志与指标，不要只做“能跑起来”的接线。

Load `references/strategy-guide.md`, `references/fastapi-backgroundtasks-patterns.md`, and `references/queue-worker-patterns.md` as needed.
