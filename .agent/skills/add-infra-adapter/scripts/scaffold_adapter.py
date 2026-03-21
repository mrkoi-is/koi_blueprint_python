#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: scaffold_adapter.py <project-root> <adapter-name> <implementation-name>")
        return 1

    project_root = Path(sys.argv[1]).resolve()
    adapter = sys.argv[2].replace("-", "_")
    impl = sys.argv[3].replace("-", "_")
    class_base = "".join(part.capitalize() for part in adapter.split("_"))

    adapter_root = project_root / "app" / "infra" / adapter
    write(adapter_root / "__init__.py", f'"""{class_base} adapter package."""\n')
    write(adapter_root / "abstract.py", f"from abc import ABC, abstractmethod\n\n\nclass Abstract{class_base}(ABC):\n    @abstractmethod\n    def ping(self) -> bool: ...\n")
    write(adapter_root / f"{impl}.py", f"from .abstract import Abstract{class_base}\n\n\nclass {''.join(part.capitalize() for part in impl.split('_'))}(Abstract{class_base}):\n    def ping(self) -> bool:\n        return True\n")
    write(adapter_root / "memory.py", f"from .abstract import Abstract{class_base}\n\n\nclass Memory{class_base}(Abstract{class_base}):\n    def ping(self) -> bool:\n        return True\n")
    print(f"[OK] Scaffolded infra adapter: {adapter}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
