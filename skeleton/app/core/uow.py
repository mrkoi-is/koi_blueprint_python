from abc import ABC, abstractmethod
from collections.abc import Callable
from types import TracebackType

from sqlalchemy.orm import Session


class AbstractUnitOfWork(ABC):
    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            self.rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy 事务工作单元。

    用法 — 子类挂载领域仓储 / Subclass to mount domain repositories::

        class DeviceUnitOfWork(SqlAlchemyUnitOfWork):
            def __enter__(self) -> "DeviceUnitOfWork":
                uow = super().__enter__()
                self.devices = SaDeviceRepository(self._session)
                return uow

        with DeviceUnitOfWork(session_factory) as uow:
            uow.devices.add(device)
            uow.commit()
    """
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        if self._session is not None:
            self._session.close()

    def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("UnitOfWork session has not been started")
        self._session.commit()

    def rollback(self) -> None:
        if self._session is None:
            return
        self._session.rollback()
