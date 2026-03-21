"""设备仓储 SQLAlchemy 2.0 实现 — 对应 architecture.md §4.5。"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Device
from .repository import AbstractDeviceRepository


class SaDeviceRepository(AbstractDeviceRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_sn(self, sn: str) -> Device | None:
        return self._session.scalar(select(Device).where(Device.sn == sn))

    def add(self, device: Device) -> None:
        self._session.add(device)

    def list_all(self, offset: int = 0, limit: int = 20) -> list[Device]:
        stmt = select(Device).offset(offset).limit(limit)
        return list(self._session.scalars(stmt))

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(Device)) or 0
