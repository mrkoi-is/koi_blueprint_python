# Async Migration Checklist

## 1. Driver 与配置

- `database_url` 改为 `postgresql+asyncpg://...`
- `pyproject.toml` 增加 `asyncpg` / `sqlalchemy[asyncio]`（按需）

## 2. Dependencies

- `create_async_engine`
- `async_sessionmaker`
- `AsyncSession`
- async session dependency

## 3. UoW

- `__aenter__` / `__aexit__`
- `commit()` / `rollback()` 改为 `async`
- 关闭 session 使用 `await`

## 4. Repository / Service / Router

- repository methods 改为 `async def`
- service methods 改为 `async def`
- route handlers 改为 `async def`
- WebSocket 路由必须异步

## 5. 验证项

- 不在 async route 中调用同步 ORM
- 不在 service 中混用 blocking I/O
- 测试覆盖至少一条异步调用链
