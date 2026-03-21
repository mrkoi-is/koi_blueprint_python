#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

KEY_FILES = [
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    "app/main.py",
    "app/config.py",
    "app/core/auth.py",
    "app/core/dependencies.py",
    "app/core/logging.py",
    "migrations/env.py",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: collect_review_inputs.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    print(f"[root] {root}")
    for rel in KEY_FILES:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    for rel in ["tests/unit", "tests/integration", ".github/workflows"]:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
