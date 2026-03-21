#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: scaffold_domain.py <project-root> <module-name>")
        return 1

    project_root = Path(sys.argv[1]).resolve()
    module = sys.argv[2].replace("-", "_")
    class_name = "".join(part.capitalize() for part in module.split("_"))

    domain_root = project_root / "app" / "domain" / module
    tests_root = project_root / "tests" / "domain" / module

    write(domain_root / "__init__.py", f'"""{class_name} domain module."""\n')
    write(domain_root / "schemas.py", f"from pydantic import BaseModel\n\n\nclass {class_name}CreateSchema(BaseModel):\n    name: str\n")
    write(domain_root / "models.py", f"from sqlalchemy.orm import Mapped, mapped_column\n\n\nclass {class_name}:\n    id: Mapped[int] = mapped_column(primary_key=True)\n")
    write(domain_root / "repository.py", f"class Abstract{class_name}Repository:\n    pass\n")
    write(domain_root / "repository_sa.py", f"from .repository import Abstract{class_name}Repository\n\n\nclass Sa{class_name}Repository(Abstract{class_name}Repository):\n    pass\n")
    write(domain_root / "uow.py", f"class {class_name}UnitOfWork:\n    pass\n")
    write(domain_root / "service.py", f"class {class_name}Service:\n    pass\n")
    write(domain_root / "router.py", f"from fastapi import APIRouter\n\nrouter = APIRouter(prefix='/{module}', tags=['{module}'])\n")
    write(tests_root / "__init__.py", "\n")
    write(tests_root / f"test_{module}_service.py", f"def test_{module}_placeholder() -> None:\n    assert True\n")

    main_file = project_root / "app" / "main.py"
    if main_file.exists():
        content = main_file.read_text(encoding="utf-8")
        import_line = f"from app.domain.{module}.router import router as {module}_router\n"
        include_line = f"    app.include_router({module}_router, prefix=api_prefix)\n"
        if import_line not in content:
            content = import_line + content
        marker = "    # register domain routers here\n"
        if marker in content and include_line not in content:
            content = content.replace(marker, marker + include_line)
        main_file.write_text(content, encoding="utf-8")

    print(f"[OK] Scaffolded domain module: {module}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
