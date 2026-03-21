#!/usr/bin/env python3
"""在现有项目中脚手架一个新的基础设施适配器。"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path


def to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scaffold_adapter(project_root: Path, adapter_name: str, impl_name: str) -> None:
    adapter_dir = project_root / "app" / "infra" / adapter_name
    test_dir = project_root / "tests" / "unit"

    if adapter_dir.exists():
        print(f"❌ 适配器目录已存在: {adapter_dir}", file=sys.stderr)
        sys.exit(1)

    pascal_adapter = to_pascal(adapter_name)
    pascal_impl = to_pascal(impl_name)

    files: dict[Path, str] = {
        adapter_dir / "__init__.py": textwrap.dedent(
            f"""\
            from .abstract import Abstract{pascal_adapter}
            from .{impl_name} import {pascal_impl}{pascal_adapter}
            from .memory import Memory{pascal_adapter}

            __all__ = [
                "Abstract{pascal_adapter}",
                "{pascal_impl}{pascal_adapter}",
                "Memory{pascal_adapter}",
            ]
            """
        ),
        adapter_dir / "abstract.py": textwrap.dedent(
            f"""\
            from abc import ABC, abstractmethod
            from typing import Any


            class Abstract{pascal_adapter}(ABC):
                @abstractmethod
                def get(self, key: str) -> Any | None: ...

                @abstractmethod
                def set(self, key: str, value: Any, ttl: int = 300) -> None: ...

                @abstractmethod
                def delete(self, key: str) -> None: ...
            """
        ),
        adapter_dir / f"{impl_name}.py": textwrap.dedent(
            f"""\
            from typing import Any

            from .abstract import Abstract{pascal_adapter}


            class {pascal_impl}{pascal_adapter}(Abstract{pascal_adapter}):
                def __init__(self, client: Any) -> None:
                    self._client = client

                def get(self, key: str) -> Any | None:
                    raise NotImplementedError("请实现 {impl_name} get 方法")

                def set(self, key: str, value: Any, ttl: int = 300) -> None:
                    raise NotImplementedError("请实现 {impl_name} set 方法")

                def delete(self, key: str) -> None:
                    raise NotImplementedError("请实现 {impl_name} delete 方法")
            """
        ),
        adapter_dir / "memory.py": textwrap.dedent(
            f"""\
            from typing import Any

            from .abstract import Abstract{pascal_adapter}


            class Memory{pascal_adapter}(Abstract{pascal_adapter}):
                def __init__(self) -> None:
                    self._store: dict[str, Any] = {{}}

                def get(self, key: str) -> Any | None:
                    return self._store.get(key)

                def set(self, key: str, value: Any, ttl: int = 300) -> None:
                    self._store[key] = value

                def delete(self, key: str) -> None:
                    self._store.pop(key, None)
            """
        ),
    }

    for path, content in files.items():
        _write(path, content)
        print(f"  ✅ 创建: {path.relative_to(project_root)}")

    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / f"test_{adapter_name}.py"
    if not test_file.exists():
        _write(
            test_file,
            textwrap.dedent(
                f"""\
                \"\"\"单元测试: Memory{pascal_adapter}\"\"\"

                from app.infra.{adapter_name} import Memory{pascal_adapter}


                def test_memory_{adapter_name}_set_get() -> None:
                    adapter = Memory{pascal_adapter}()
                    adapter.set("key1", {{"data": "value"}})
                    assert adapter.get("key1") == {{"data": "value"}}


                def test_memory_{adapter_name}_delete() -> None:
                    adapter = Memory{pascal_adapter}()
                    adapter.set("key1", "value")
                    adapter.delete("key1")
                    assert adapter.get("key1") is None
                """
            ),
        )
        print(f"  ✅ 创建: tests/unit/test_{adapter_name}.py")

    print(f"\n✅ 适配器 '{adapter_name}' ({impl_name} 实现) 脚手架完成")


def main() -> None:
    parser = argparse.ArgumentParser(description="Koi 基础设施适配器脚手架")
    parser.add_argument("project_root", type=Path, help="项目根目录")
    parser.add_argument("adapter_name", help="适配器名 (snake_case)")
    parser.add_argument("impl_name", help="实现名 (如 redis, qiniu, mqtt)")
    args = parser.parse_args()
    scaffold_adapter(args.project_root, args.adapter_name, args.impl_name)


if __name__ == "__main__":
    main()
