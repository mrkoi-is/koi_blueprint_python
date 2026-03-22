#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PATTERNS = [
    "slowapi",
    "Limiter",
    "429",
    "rate limit",
    "/health",
    "/metrics",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_rate_limit_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    print(f"[root] {root}")
    files = list(root.rglob("*.py"))
    for rel in ["app/main.py", "pyproject.toml", "tests"]:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {rel}")
    print("[signals]")
    for pattern in PATTERNS:
        found = any(pattern in path.read_text(encoding="utf-8", errors="ignore") for path in files)
        print(f"- {pattern}: {'YES' if found else 'NO'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
