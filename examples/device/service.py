"""设备服务 — 纯 Python 业务逻辑，不依赖 Web 框架或 ORM。

对应 architecture.md §4.5 标准模式：
- 依赖 UoW 抽象而非具体实现
- 使用 with self._uow: 上下文管理器确保异常自动回滚
"""

from app.core.exceptions import ConflictError

from .models import Device
from .uow import DeviceUnitOfWork


class DeviceService:
    def __init__(self, uow: DeviceUnitOfWork) -> None:
        self._uow = uow

    def register(self, sn: str, name: str) -> Device:
        with self._uow:
            if self._uow.devices.get_by_sn(sn):
                raise ConflictError("Device already exists")
            device = Device(sn=sn, name=name)
            self._uow.devices.add(device)
            self._uow.commit()
            return device

    def list(self, offset: int = 0, limit: int = 20) -> tuple[list[Device], int]:
        with self._uow:
            items = self._uow.devices.list_all(offset=offset, limit=limit)
            total = self._uow.devices.count()
            return items, total
