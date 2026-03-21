"""异步依赖注入示例

演示 create_async_engine + async_sessionmaker + AsyncSession
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 使用 asyncpg 驱动
# database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/koi_service"
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/koi_service"

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
