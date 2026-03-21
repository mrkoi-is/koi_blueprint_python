from abc import ABC, abstractmethod

from .models import Device


class AbstractDeviceRepository(ABC):
    @abstractmethod
    def get_by_sn(self, sn: str) -> Device | None: ...

    @abstractmethod
    def add(self, device: Device) -> None: ...

    @abstractmethod
    def list_all(self) -> list[Device]: ...
