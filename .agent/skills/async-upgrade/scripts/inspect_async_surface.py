#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

CHECKS = [
    "pyproject.toml",
    "app/core/dependencies.py",
    "app/core/uow.py",
]

PATTERNS = [
    "create_async_engine",
    "async_sessionmaker",
    "AsyncSession",
    "postgresql+asyncpg://",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_async_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    print(f"[root] {root}")
    for rel in CHECKS:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    print("[signals]")
    for pattern in PATTERNS:
        found = any(
            pattern in path.read_text(encoding="utf-8", errors="ignore")
            for path in root.rglob("*.py")
        )
        print(f"- {pattern}: {'YES' if found else 'NO'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
