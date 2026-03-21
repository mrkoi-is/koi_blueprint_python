#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PATTERNS = [
    '/api/v1',
    '/api/v2',
    'api_prefix',
    'include_router',
]


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: inspect_versioning_surface.py <target-root>')
        return 1

    root = Path(sys.argv[1]).resolve()
    main_file = root / 'app' / 'main.py'
    print(f'[root] {root}')
    print(f"[{'OK' if main_file.exists() else 'NO'}] app/main.py")
    print('[signals]')
    files = list(root.rglob('*.py'))
    for pattern in PATTERNS:
        found = any(pattern in path.read_text(encoding='utf-8', errors='ignore') for path in files)
        print(f'- {pattern}: {"YES" if found else "NO"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
