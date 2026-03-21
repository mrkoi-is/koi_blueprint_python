#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def contains(path: Path, needle: str) -> bool:
    return path.is_file() and needle in path.read_text(encoding="utf-8")


def any_file(root: Path, pattern: str) -> bool:
    return any(root.glob(pattern))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_background_task_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    pyproject = root / "pyproject.toml"
    main_py = root / "app" / "main.py"
    compose_candidates = [
        root / "docker-compose.yml",
        root / "compose.yml",
        root / "compose.yaml",
    ]

    result = {
        "root": str(root),
        "has_pyproject": pyproject.is_file(),
        "uses_backgroundtasks": contains(main_py, "BackgroundTasks")
        or any("BackgroundTasks" in path.read_text(encoding="utf-8") for path in (root / "app").rglob("*.py")),
        "has_celery_dependency": contains(pyproject, "celery"),
        "has_arq_dependency": contains(pyproject, "arq"),
        "has_worker_module": any_file(root / "app", "worker.py") or any_file(root / "app", "**/worker.py"),
        "has_task_module": any_file(root / "app", "**/tasks.py"),
        "has_compose_file": any(path.is_file() for path in compose_candidates),
        "compose_mentions_worker": any(path.is_file() and "worker" in path.read_text(encoding="utf-8") for path in compose_candidates),
        "compose_mentions_redis": any(path.is_file() and "redis" in path.read_text(encoding="utf-8") for path in compose_candidates),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
