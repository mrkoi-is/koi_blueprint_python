#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def contains(path: Path, needle: str) -> bool:
    return path.is_file() and needle in path.read_text(encoding="utf-8")


def any_contains(root: Path, needle: str) -> bool:
    return any(needle in path.read_text(encoding="utf-8") for path in root.rglob("*.py"))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_websocket_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    app_root = root / "app"
    tests_root = root / "tests"
    auth_py = app_root / "core" / "auth.py"

    result = {
        "root": str(root),
        "has_websocket_route": any_contains(app_root, "@router.websocket") if app_root.is_dir() else False,
        "uses_websocket_class": any_contains(app_root, "WebSocket") if app_root.is_dir() else False,
        "has_connection_manager": any_contains(app_root, "ConnectionManager") if app_root.is_dir() else False,
        "mentions_websocket_disconnect": any_contains(app_root, "WebSocketDisconnect") if app_root.is_dir() else False,
        "has_auth_module": auth_py.is_file(),
        "auth_mentions_token": contains(auth_py, "token") or contains(auth_py, "Bearer"),
        "has_websocket_tests": any("websocket_connect" in path.read_text(encoding="utf-8") for path in tests_root.rglob("*.py")) if tests_root.is_dir() else False,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
