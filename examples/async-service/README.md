# async-service 异步服务示例

演示完整的异步路径：`AsyncSession` + `create_async_engine` + `asyncpg`。

## 与同步的区别

| 同步 (默认) | 异步 |
|---|---|
| `create_engine` | `create_async_engine` |
| `Session` | `AsyncSession` |
| `sessionmaker` | `async_sessionmaker` |
| `psycopg` | `asyncpg` |
| `def endpoint` | `async def endpoint` |
| `with uow:` | `async with uow:` |

## 依赖

```bash
uv add asyncpg sqlalchemy[asyncio]
```

## 所需修改

1. `config.py` — `database_url` 使用 `postgresql+asyncpg://...`
2. `dependencies.py` — 使用 `create_async_engine` + `async_sessionmaker`
3. `uow.py` — 使用异步上下文管理器 (`__aenter__` / `__aexit__`)
4. `repository_sa.py` — 方法全部 `async def`
5. `service.py` — 方法全部 `async def`
6. `router.py` — 路由函数全部 `async def`
