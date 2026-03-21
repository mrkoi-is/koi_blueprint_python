#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path


def copy_contents(source: Path, target: Path) -> None:
    for item in source.iterdir():
        destination = target / item.name
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: apply_skeleton.py <target-project-root>")
        return 1

    target_root = Path(sys.argv[1]).resolve()
    blueprint_root = Path(__file__).resolve().parents[4]
    skeleton_root = blueprint_root / "skeleton"

    if not target_root.exists():
        raise FileNotFoundError(f"Target project root does not exist: {target_root}")

    copy_contents(skeleton_root, target_root)
    print(f"[OK] Copied skeleton from {skeleton_root} to {target_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
