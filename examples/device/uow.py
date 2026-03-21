"""领域级 UoW — 继承 SqlAlchemyUnitOfWork，在 __enter__ 中挂载本领域的 Repository。

对应 architecture.md §4.5 标准模式。
"""

from __future__ import annotations

from app.core.uow import SqlAlchemyUnitOfWork

from .repository import AbstractDeviceRepository
from .repository_sa import SaDeviceRepository


class DeviceUnitOfWork(SqlAlchemyUnitOfWork):
    devices: AbstractDeviceRepository

    def __enter__(self) -> DeviceUnitOfWork:
        super().__enter__()
        assert self._session is not None
        self.devices = SaDeviceRepository(self._session)
        return self
