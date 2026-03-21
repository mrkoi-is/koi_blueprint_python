#!/usr/bin/env python3
"""在现有项目中脚手架一个新的基础设施适配器。

用法:
    python scripts/scaffold_adapter.py <project-root> <adapter-name> <implementation-name>

示例:
    python scripts/scaffold_adapter.py /path/to/my-service cache redis
    → 生成 app/infra/cache.py (抽象接口 + Redis 实现 + Memory 替身)
"""
import argparse
import sys
import textwrap
from pathlib import Path


def to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def scaffold_adapter(project_root: Path, adapter_name: str, impl_name: str) -> None:
    infra_dir = project_root / "app" / "infra"
    test_dir = project_root / "tests" / "unit"

    infra_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    adapter_file = infra_dir / f"{adapter_name}.py"
    if adapter_file.exists():
        print(f"❌ 适配器文件已存在: {adapter_file}", file=sys.stderr)
        sys.exit(1)

    pascal_adapter = to_pascal(adapter_name)
    pascal_impl = to_pascal(impl_name)

    content = textwrap.dedent(f"""\
        \"\"\"基础设施适配器: {adapter_name}

        抽象接口 + {impl_name} 实现 + Memory 替身
        \"\"\"
        from abc import ABC, abstractmethod
        from typing import Any


        class Abstract{pascal_adapter}(ABC):
            \"\"\"抽象接口 — Service 层只依赖此接口\"\"\"

            @abstractmethod
            def get(self, key: str) -> Any | None: ...

            @abstractmethod
            def set(self, key: str, value: Any, ttl: int = 300) -> None: ...

            @abstractmethod
            def delete(self, key: str) -> None: ...


        class {pascal_impl}{pascal_adapter}(Abstract{pascal_adapter}):
            \"\"\"生产实现 — 连接真实的 {impl_name} 服务\"\"\"

            def __init__(self, client: Any) -> None:
                self._client = client

            def get(self, key: str) -> Any | None:
                raise NotImplementedError("请实现 {impl_name} get 方法")

            def set(self, key: str, value: Any, ttl: int = 300) -> None:
                raise NotImplementedError("请实现 {impl_name} set 方法")

            def delete(self, key: str) -> None:
                raise NotImplementedError("请实现 {impl_name} delete 方法")


        class Memory{pascal_adapter}(Abstract{pascal_adapter}):
            \"\"\"内存替身 — 用于单元测试\"\"\"

            def __init__(self) -> None:
                self._store: dict[str, Any] = {{}}

            def get(self, key: str) -> Any | None:
                return self._store.get(key)

            def set(self, key: str, value: Any, ttl: int = 300) -> None:
                self._store[key] = value

            def delete(self, key: str) -> None:
                self._store.pop(key, None)
    """)

    adapter_file.write_text(content, encoding="utf-8")
    print(f"  ✅ 创建: app/infra/{adapter_name}.py")

    # 测试桩
    test_file = test_dir / f"test_{adapter_name}.py"
    if not test_file.exists():
        test_file.write_text(
            textwrap.dedent(f"""\
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
            """),
            encoding="utf-8",
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
