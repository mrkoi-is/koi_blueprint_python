#!/usr/bin/env python3
"""在现有项目中脚手架一个新的领域模块。"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path


def to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def _pluralize(name: str) -> str:
    return name if name.endswith("s") else f"{name}s"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scaffold_domain(project_root: Path, module_name: str) -> None:
    module_dir = project_root / "app" / "domain" / module_name
    test_dir = project_root / "tests" / "unit"

    if module_dir.exists():
        print(f"❌ 模块目录已存在: {module_dir}", file=sys.stderr)
        sys.exit(1)

    pascal = to_pascal(module_name)
    repo_attr = _pluralize(module_name)
    table_name = _pluralize(module_name)

    module_dir.mkdir(parents=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    files: dict[str, str] = {
        "__init__.py": f'"""领域模块: {module_name}"""\n',
        "models.py": textwrap.dedent(
            f"""\
            from sqlalchemy import String
            from sqlalchemy.orm import Mapped, mapped_column

            from app.core.db import Base


            class {pascal}(Base):
                __tablename__ = \"{table_name}\"

                id: Mapped[int | None] = mapped_column(primary_key=True, autoincrement=True)
                name: Mapped[str] = mapped_column(String(128), index=True)
            """
        ),
        "schemas.py": textwrap.dedent(
            f"""\
            from pydantic import BaseModel


            class {pascal}CreateSchema(BaseModel):
                name: str


            class {pascal}Schema(BaseModel):
                id: int
                name: str

                model_config = {{"from_attributes": True}}
            """
        ),
        "repository.py": textwrap.dedent(
            f"""\
            from typing import Protocol

            from app.domain.{module_name}.models import {pascal}


            class {pascal}Repository(Protocol):
                def get(self, id: int) -> {pascal} | None: ...
                def add(self, entity: {pascal}) -> None: ...
                def list_all(self, offset: int = 0, limit: int = 20) -> list[{pascal}]: ...
                def count(self) -> int: ...
            """
        ),
        "repository_sa.py": textwrap.dedent(
            f"""\
            from sqlalchemy import func, select
            from sqlalchemy.orm import Session

            from app.domain.{module_name}.models import {pascal}


            class Sa{pascal}Repository:
                def __init__(self, session: Session) -> None:
                    self._session = session

                def get(self, id: int) -> {pascal} | None:
                    return self._session.get({pascal}, id)

                def add(self, entity: {pascal}) -> None:
                    self._session.add(entity)

                def list_all(self, offset: int = 0, limit: int = 20) -> list[{pascal}]:
                    stmt = select({pascal}).offset(offset).limit(limit)
                    return list(self._session.scalars(stmt))

                def count(self) -> int:
                    stmt = select(func.count()).select_from({pascal})
                    return self._session.scalar(stmt) or 0
            """
        ),
        "uow.py": textwrap.dedent(
            f"""\
            from app.core.uow import SqlAlchemyUnitOfWork
            from app.domain.{module_name}.repository_sa import Sa{pascal}Repository


            class {pascal}UnitOfWork(SqlAlchemyUnitOfWork):
                {repo_attr}: Sa{pascal}Repository

                def __enter__(self) -> "{pascal}UnitOfWork":
                    super().__enter__()
                    assert self._session is not None
                    self.{repo_attr} = Sa{pascal}Repository(self._session)
                    return self
            """
        ),
        "service.py": textwrap.dedent(
            f"""\
            from app.core.exceptions import NotFoundError
            from app.domain.{module_name}.models import {pascal}
            from app.domain.{module_name}.uow import {pascal}UnitOfWork


            class {pascal}Service:
                def __init__(self, uow: {pascal}UnitOfWork) -> None:
                    self._uow = uow

                def create(self, name: str) -> {pascal}:
                    with self._uow:
                        entity = {pascal}(name=name)
                        self._uow.{repo_attr}.add(entity)
                        self._uow.commit()
                        return entity

                def get_or_raise(self, id: int) -> {pascal}:
                    with self._uow:
                        entity = self._uow.{repo_attr}.get(id)
                        if entity is None:
                            raise NotFoundError(f"{pascal} {{id}} not found")
                        return entity

                def list(self, offset: int, limit: int) -> tuple[list[{pascal}], int]:
                    with self._uow:
                        items = self._uow.{repo_attr}.list_all(offset=offset, limit=limit)
                        total = self._uow.{repo_attr}.count()
                        return items, total
            """
        ),
        "router.py": textwrap.dedent(
            f"""\
            from collections.abc import Callable

            from fastapi import APIRouter, Depends, status
            from sqlalchemy.orm import Session

            from app.core.dependencies import get_session_factory
            from app.core.pagination import PaginationParams
            from app.core.responses import ApiResponse, PaginatedData
            from app.domain.{module_name}.schemas import {pascal}CreateSchema, {pascal}Schema
            from app.domain.{module_name}.service import {pascal}Service
            from app.domain.{module_name}.uow import {pascal}UnitOfWork

            router = APIRouter(prefix="/{table_name}", tags=["{table_name}"])


            def get_{module_name}_service(
                session_factory: Callable[[], Session] = Depends(get_session_factory),
            ) -> {pascal}Service:
                return {pascal}Service({pascal}UnitOfWork(session_factory))


            @router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[{pascal}Schema])
            def create_{module_name}(
                payload: {pascal}CreateSchema,
                service: {pascal}Service = Depends(get_{module_name}_service),
            ) -> ApiResponse[{pascal}Schema]:
                entity = service.create(payload.name)
                return ApiResponse(data=entity)


            @router.get("/", response_model=ApiResponse[PaginatedData[{pascal}Schema]])
            def list_{table_name}(
                pagination: PaginationParams = Depends(),
                service: {pascal}Service = Depends(get_{module_name}_service),
            ) -> ApiResponse[PaginatedData[{pascal}Schema]]:
                items, total = service.list(pagination.offset, pagination.page_size)
                return ApiResponse(
                    data=PaginatedData(
                        items=items,
                        total=total,
                        page=pagination.page,
                        page_size=pagination.page_size,
                    )
                )
            """
        ),
    }

    for filename, content in files.items():
        _write(module_dir / filename, content)
        print(f"  ✅ 创建: app/domain/{module_name}/{filename}")

    test_file = test_dir / f"test_{module_name}_service.py"
    if not test_file.exists():
        _write(
            test_file,
            textwrap.dedent(
                f"""\
                \"\"\"单元测试: {pascal}Service\"\"\"

                from typing import cast

                from app.core.repository import MemoryRepository
                from app.domain.{module_name}.models import {pascal}
                from app.domain.{module_name}.service import {pascal}Service
                from app.domain.{module_name}.uow import {pascal}UnitOfWork


                class Memory{pascal}Repository(MemoryRepository[{pascal}]):
                    pass


                class Fake{pascal}UnitOfWork:
                    def __init__(self) -> None:
                        self.{repo_attr} = Memory{pascal}Repository()
                        self.committed = False

                    def __enter__(self) -> "Fake{pascal}UnitOfWork":
                        return self

                    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
                        if exc_type:
                            self.rollback()

                    def commit(self) -> None:
                        self.committed = True

                    def rollback(self) -> None:
                        return None


                def test_{module_name}_create() -> None:
                    uow = Fake{pascal}UnitOfWork()
                    service = {pascal}Service(cast({pascal}UnitOfWork, uow))

                    entity = service.create("demo")

                    assert entity.id == 1
                    assert entity.name == "demo"
                    assert uow.committed is True


                def test_{module_name}_list() -> None:
                    uow = Fake{pascal}UnitOfWork()
                    service = {pascal}Service(cast({pascal}UnitOfWork, uow))
                    service.create("demo-1")
                    service.create("demo-2")

                    items, total = service.list(0, 20)

                    assert total == 2
                    assert [item.name for item in items] == ["demo-1", "demo-2"]
                """
            ),
        )
        print(f"  ✅ 创建: tests/unit/test_{module_name}_service.py")

    main_file = project_root / "app" / "main.py"
    if main_file.exists():
        content = main_file.read_text(encoding="utf-8")
        import_line = f"from app.domain.{module_name}.router import router as {module_name}_router\n"
        include_line = f"    app.include_router({module_name}_router, prefix=api_prefix)\n"
        marker = "    # 在此注册领域路由 / register domain routers here\n"
        if import_line not in content:
            content = import_line + content
        if marker in content and include_line not in content:
            content = content.replace(marker, marker + include_line)
        main_file.write_text(content, encoding="utf-8")
        print(f"  ✅ 更新: app/main.py (注册 {module_name}_router)")

    print(f"\n✅ 领域模块 '{module_name}' 脚手架完成")


def main() -> None:
    parser = argparse.ArgumentParser(description="Koi 领域模块脚手架")
    parser.add_argument("project_root", type=Path, help="项目根目录")
    parser.add_argument("module_name", help="模块名 (snake_case)")
    args = parser.parse_args()
    scaffold_domain(args.project_root, args.module_name)


if __name__ == "__main__":
    main()
