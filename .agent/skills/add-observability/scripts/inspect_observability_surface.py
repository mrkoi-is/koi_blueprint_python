#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def contains(path: Path, needle: str) -> bool:
    return path.is_file() and needle in path.read_text(encoding="utf-8")


def compose_mentions(paths: list[Path], needle: str) -> bool:
    return any(path.is_file() and needle in path.read_text(encoding="utf-8") for path in paths)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_observability_surface.py <target-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    pyproject = root / "pyproject.toml"
    main_py = root / "app" / "main.py"
    logging_py = root / "app" / "core" / "logging.py"
    metrics_py = root / "app" / "core" / "metrics.py"
    compose_files = [
        root / "docker-compose.yml",
        root / "compose.yml",
        root / "compose.yaml",
    ]

    result = {
        "root": str(root),
        "has_pyproject": pyproject.is_file(),
        "uses_structlog": contains(logging_py, "structlog") or contains(pyproject, "structlog"),
        "has_metrics_module": metrics_py.is_file(),
        "main_mentions_metrics": contains(main_py, "metrics") or contains(main_py, "setup_metrics"),
        "has_prometheus_dependency": contains(pyproject, "prometheus-fastapi-instrumentator")
        or contains(pyproject, "prometheus_client"),
        "has_otel_dependency": contains(pyproject, "opentelemetry"),
        "main_mentions_tracing": contains(main_py, "tracing")
        or contains(main_py, "FastAPIInstrumentor"),
        "has_compose_file": any(path.is_file() for path in compose_files),
        "has_prometheus_asset": compose_mentions(compose_files, "prometheus"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
