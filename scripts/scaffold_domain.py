#!/usr/bin/env python3
"""在现有项目中脚手架一个新的领域模块。

用法:
    python scripts/scaffold_domain.py <project-root> <module-name>

示例:
    python scripts/scaffold_domain.py /path/to/my-service store
    → 生成 app/domain/store/{__init__.py, router.py, schemas.py, models.py, service.py, repository.py, repository_sa.py, uow.py}
    → 生成 tests/domain/test_store_service.py
"""
import argparse
import sys
import textwrap
from pathlib import Path


def to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def scaffold_domain(project_root: Path, module_name: str) -> None:
    module_dir = project_root / "app" / "domain" / module_name
    test_dir = project_root / "tests" / "domain"

    if module_dir.exists():
        print(f"❌ 模块目录已存在: {module_dir}", file=sys.stderr)
        sys.exit(1)

    pascal = to_pascal(module_name)
    module_dir.mkdir(parents=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    files: dict[str, str] = {
        "__init__.py": f'"""领域模块: {module_name}"""\n',
        "models.py": textwrap.dedent(f"""\
            from sqlalchemy import String
            from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


            class Base(DeclarativeBase):
                pass


            class {pascal}(Base):
                __tablename__ = "{module_name}s"

                id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
                name: Mapped[str] = mapped_column(String(128))
        """),
        "schemas.py": textwrap.dedent(f"""\
            from pydantic import BaseModel


            class {pascal}CreateSchema(BaseModel):
                name: str


            class {pascal}Schema(BaseModel):
                id: int
                name: str

                model_config = {{"from_attributes": True}}
        """),
        "repository.py": textwrap.dedent(f"""\
            from typing import Protocol

            from app.domain.{module_name}.models import {pascal}


            class {pascal}Repository(Protocol):
                def get(self, id: int) -> {pascal} | None: ...
                def add(self, entity: {pascal}) -> None: ...
                def list_all(self, offset: int = 0, limit: int = 20) -> list[{pascal}]: ...
                def count(self) -> int: ...
        """),
        "repository_sa.py": textwrap.dedent(f"""\
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
        """),
        "uow.py": textwrap.dedent(f"""\
            from app.core.uow import SqlAlchemyUnitOfWork
            from app.domain.{module_name}.repository_sa import Sa{pascal}Repository


            class {pascal}UnitOfWork(SqlAlchemyUnitOfWork):
                {module_name}s: Sa{pascal}Repository

                def __enter__(self) -> \"{pascal}UnitOfWork\":
                    super().__enter__()
                    assert self._session is not None
                    self.{module_name}s = Sa{pascal}Repository(self._session)
                    return self
        """),
        "service.py": textwrap.dedent(f"""\
            from app.core.exceptions import ConflictError, NotFoundError
            from app.domain.{module_name}.models import {pascal}
            from app.domain.{module_name}.uow import {pascal}UnitOfWork


            class {pascal}Service:
                def __init__(self, uow: {pascal}UnitOfWork) -> None:
                    self._uow = uow

                def create(self, name: str) -> {pascal}:
                    with self._uow:
                        entity = {pascal}(name=name)
                        self._uow.{module_name}s.add(entity)
                        self._uow.commit()
                        return entity

                def get_or_raise(self, id: int) -> {pascal}:
                    with self._uow:
                        entity = self._uow.{module_name}s.get(id)
                        if entity is None:
                            raise NotFoundError(f\"{pascal} {{id}} not found\")
                        return entity

                def list(self, offset: int, limit: int) -> tuple[list[{pascal}], int]:
                    with self._uow:
                        items = self._uow.{module_name}s.list_all(offset=offset, limit=limit)
                        total = self._uow.{module_name}s.count()
                        return items, total
        """),
        "router.py": textwrap.dedent(f"""\
            from fastapi import APIRouter, Depends

            from app.core.pagination import PaginationParams
            from app.core.responses import ApiResponse, PaginatedData
            from app.domain.{module_name}.schemas import {pascal}CreateSchema, {pascal}Schema

            router = APIRouter(prefix=\"/{module_name}s\", tags=[\"{module_name}s\"])


            @router.post(\"/\", status_code=201, response_model=ApiResponse[{pascal}Schema])
            def create_{module_name}(payload: {pascal}CreateSchema):
                # TODO: 注入 Service via Depends
                raise NotImplementedError


            @router.get(\"/\", response_model=ApiResponse[PaginatedData[{pascal}Schema]])
            def list_{module_name}s(pagination: PaginationParams = Depends()):
                # TODO: 注入 Service via Depends
                raise NotImplementedError
        """),
    }

    for filename, content in files.items():
        (module_dir / filename).write_text(content, encoding="utf-8")
        print(f"  ✅ 创建: app/domain/{module_name}/{filename}")

    # 生成测试桩
    test_file = test_dir / f"test_{module_name}_service.py"
    if not test_file.exists():
        test_file.write_text(
            textwrap.dedent(f"""\
                \"\"\"单元测试: {pascal}Service\"\"\"


                def test_{module_name}_create_placeholder() -> None:
                    # TODO: 使用 MemoryRepository 替身测试业务逻辑
                    assert True
            """),
            encoding="utf-8",
        )
        print(f"  ✅ 创建: tests/domain/test_{module_name}_service.py")

    print(f"\n✅ 领域模块 '{module_name}' 脚手架完成")
    print(f"   下一步: 在 app/main.py 注册 router，运行 ruff + pyright + pytest")


def main() -> None:
    parser = argparse.ArgumentParser(description="Koi 领域模块脚手架")
    parser.add_argument("project_root", type=Path, help="项目根目录")
    parser.add_argument("module_name", help="模块名 (snake_case)")
    args = parser.parse_args()
    scaffold_domain(args.project_root, args.module_name)


if __name__ == "__main__":
    main()
