"""通用 CRUD Repository 基类

减少领域模块中 80%+ 的样板代码。
领域模块只需继承并添加业务特定的查询方法。
"""
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    """泛型仓储抽象接口 — Service 层只依赖此接口"""

    @abstractmethod
    def get(self, id: int) -> T | None: ...

    @abstractmethod
    def add(self, entity: T) -> None: ...

    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 20, **filters: Any) -> list[T]: ...

    @abstractmethod
    def count(self, **filters: Any) -> int: ...

    @abstractmethod
    def delete(self, entity: T) -> None: ...


class SaRepository(AbstractRepository[T]):
    """SQLAlchemy 2.0 通用实现

    用法:
        class SaDeviceRepository(SaRepository[Device]):
            model_class = Device

            def get_by_sn(self, sn: str) -> Device | None:
                stmt = select(Device).where(Device.sn == sn)
                return self._session.scalar(stmt)
    """

    model_class: type[T]

    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, id: int) -> T | None:
        return self._session.get(self.model_class, id)

    def add(self, entity: T) -> None:
        self._session.add(entity)

    def list_all(self, offset: int = 0, limit: int = 20, **filters: Any) -> list[T]:
        stmt = select(self.model_class)
        stmt = self._apply_filters(stmt, **filters)
        stmt = stmt.offset(offset).limit(limit)
        return list(self._session.scalars(stmt))

    def count(self, **filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model_class)
        stmt = self._apply_filters(stmt, **filters)
        return self._session.scalar(stmt) or 0

    def delete(self, entity: T) -> None:
        self._session.delete(entity)

    def _apply_filters(self, stmt: Any, **filters: Any) -> Any:
        """子类可覆盖此方法以支持领域特定的过滤逻辑"""
        return stmt


class MemoryRepository(AbstractRepository[T]):
    """内存替身 — 用于单元测试，无需依赖数据库"""

    def __init__(self) -> None:
        self._store: dict[int, T] = {}
        self._next_id = 1

    def get(self, id: int) -> T | None:
        return self._store.get(id)

    def add(self, entity: T) -> None:
        entity_obj = entity
        if not hasattr(entity_obj, "id") or entity_obj.id is None:  # type: ignore[attr-defined]
            object.__setattr__(entity_obj, "id", self._next_id)
            self._next_id += 1
        self._store[entity_obj.id] = entity  # type: ignore[attr-defined]

    def list_all(self, offset: int = 0, limit: int = 20, **filters: Any) -> list[T]:
        items = list(self._store.values())
        return items[offset : offset + limit]

    def count(self, **filters: Any) -> int:
        return len(self._store)

    def delete(self, entity: T) -> None:
        entity_id = getattr(entity, "id", None)
        if entity_id is not None:
            self._store.pop(entity_id, None)
