from sqlalchemy.orm import Session

from .repository_sa import SaDeviceRepository


class DeviceUnitOfWork:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.devices = SaDeviceRepository(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
