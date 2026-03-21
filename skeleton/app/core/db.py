from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """共享 ORM Base。

    领域模型统一继承此 Base，便于 Alembic 自动发现 metadata。
    """
