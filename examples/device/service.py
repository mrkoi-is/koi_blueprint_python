from app.core.exceptions import ConflictError

from .models import Device
from .uow import DeviceUnitOfWork


class DeviceService:
    def __init__(self, uow: DeviceUnitOfWork) -> None:
        self._uow = uow

    def register(self, sn: str, name: str) -> Device:
        if self._uow.devices.get_by_sn(sn):
            raise ConflictError("Device already exists")
        device = Device(sn=sn, name=name)
        self._uow.devices.add(device)
        self._uow.commit()
        return device

    def list(self) -> list[Device]:
        return self._uow.devices.list_all()
