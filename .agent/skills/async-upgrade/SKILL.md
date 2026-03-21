---
name: async-upgrade
description: Upgrade a Koi-standard Python service from sync-first patterns to async-ready architecture. Use when introducing AsyncSession, create_async_engine, async repositories, async unit of work, async route handlers, websocket-ready flows, or when auditing sync/async boundaries in FastAPI services.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 把同步 FastAPI 服务升级为异步实现
- 引入 `AsyncSession` / `asyncpg`
- 审查 sync / async 边界是否正确
- 为 WebSocket、长连接或高并发 I/O 做异步改造

## Workflow

1. Read `docs/architecture.md` sync vs async section and `examples/async-service/`.
2. Inspect the target project's:
   - `app/core/dependencies.py`
   - `app/core/uow.py`
   - `app/domain/*/repository_sa.py`
   - `app/domain/*/service.py`
   - `app/domain/*/router.py`
   - `pyproject.toml`
3. Run `scripts/inspect_async_surface.py <target-root>` to gather current sync/async signals.
4. Compare current code against `references/async-migration-checklist.md`.
5. Upgrade in this order:
   - database URL / driver
   - engine / session factory
   - UoW
   - repository methods
   - service methods
   - route handlers
6. Use `references/sync-async-boundaries.md` to avoid mixed blocking code in async handlers.
7. Validate behavior and keep the change set cohesive; do not mix unrelated refactors.

## Upgrade Principles

- 只有在确有高并发 I/O 需求时才切异步。
- 不要在 `async def` 中保留同步 ORM / 阻塞 I/O。
- 同一个调用链应尽量保持一致：engine → session → repo → service → router。
- 若项目只是普通 CRUD，同步实现通常仍是首选。

Load `references/async-migration-checklist.md` and `references/sync-async-boundaries.md` when needed.
