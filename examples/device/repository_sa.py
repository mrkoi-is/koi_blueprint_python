from sqlalchemy import select
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

    def list_all(self) -> list[Device]:
        return list(self._session.scalars(select(Device)).all())
