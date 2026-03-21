"""异步 Repository 示例

演示使用 AsyncSession 的 Repository 异步实现
"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class AsyncSaRepository:
    """异步 SQLAlchemy Repository 基类示例

    具体使用时替换 model_class 为实际 ORM 模型
    """

    model_class = None  # type: ignore  # 子类设置

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, id: int):
        return await self._session.get(self.model_class, id)

    async def add(self, entity) -> None:
        self._session.add(entity)

    async def list_all(self, offset: int = 0, limit: int = 20) -> list:
        stmt = select(self.model_class).offset(offset).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result)

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model_class)
        result = await self._session.scalar(stmt)
        return result or 0
