"""设备仓储抽象接口 — 对应 architecture.md §4.5。"""

from abc import ABC, abstractmethod

from .models import Device


class AbstractDeviceRepository(ABC):
    @abstractmethod
    def get_by_sn(self, sn: str) -> Device | None: ...

    @abstractmethod
    def add(self, device: Device) -> None: ...

    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 20) -> list[Device]: ...

    @abstractmethod
    def count(self) -> int: ...
