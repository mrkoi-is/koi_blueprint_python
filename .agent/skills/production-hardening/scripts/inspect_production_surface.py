#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

CHECKS = [
    "pyproject.toml",
    "uv.lock",
    "Dockerfile",
    ".dockerignore",
    ".env.example",
    "docker-compose.yml",
    ".github/workflows",
    "app/main.py",
    "app/core/logging.py",
    "app/core/metrics.py",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_production_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    print(f"[root] {root}")
    for rel in CHECKS:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
