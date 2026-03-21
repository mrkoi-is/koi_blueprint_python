#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PATTERNS = [
    ("app/core/auth.py", "auth core"),
    ("app/core/exceptions.py", "exceptions"),
    ("app/core/exception_handlers.py", "exception handlers"),
    ("tests/unit/test_auth.py", "auth unit tests"),
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_auth_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    for rel, label in PATTERNS:
        path = root / rel
        print(f"[{'OK' if path.exists() else 'NO'}] {label}: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
