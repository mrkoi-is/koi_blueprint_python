"""异步 UoW 示例

演示使用 AsyncSession 的 Unit of Work 异步版本
"""
from abc import ABC, abstractmethod
from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession


class AsyncAbstractUnitOfWork(ABC):
    async def __aenter__(self) -> "AsyncAbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class AsyncSqlAlchemyUnitOfWork(AsyncAbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "AsyncSqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        if self._session is not None:
            await self._session.close()

    async def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("UnitOfWork session has not been started")
        await self._session.commit()

    async def rollback(self) -> None:
        if self._session is None:
            return
        await self._session.rollback()
