---
name: add-background-task
description: Add background task infrastructure to a Koi-standard Python service. Use when integrating Celery, ARQ or FastAPI BackgroundTasks for asynchronous job processing such as email sending, report generation, or data synchronization.
---

> 适配 `docs/architecture.md` v4.0

## Choosing a Strategy

| Strategy | When to Use |
|---|---|
| **FastAPI BackgroundTasks** | 简单任务，不需要持久化或重试（如发送通知邮件） |
| **ARQ** (async Redis queue) | 中等复杂度，需要 Redis 队列但不需要 Celery 的全部功能 |
| **Celery** | 企业级，需要定时任务、重试策略、多 Worker、结果后端 |

## Workflow (Celery)

1. 安装依赖: `uv add celery[redis]`
2. 创建 `app/worker.py`:
   ```python
   from celery import Celery
   from app.config import settings

   celery_app = Celery("worker", broker=settings.redis_url)
   celery_app.autodiscover_tasks(["app.domain"])
   ```
3. 在领域模块添加 `tasks.py`:
   ```python
   from app.worker import celery_app

   @celery_app.task
   def send_notification(user_id: int, message: str) -> None:
       # 业务逻辑
       pass
   ```
4. 在 `docker-compose.yml` 添加 Worker 服务
5. 运行: `celery -A app.worker worker --loglevel=info`

## Workflow (FastAPI BackgroundTasks)

1. 无需额外依赖
2. 在 router 中注入 `BackgroundTasks`:
   ```python
   from fastapi import BackgroundTasks

   @router.post("/notify")
   def notify(bg: BackgroundTasks):
       bg.add_task(send_email, "user@example.com")
       return {"status": "queued"}
   ```
