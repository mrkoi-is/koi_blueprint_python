#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_test_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    for rel in ["tests", "tests/unit", "tests/integration", "tests/conftest.py", "pyproject.toml"]:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
