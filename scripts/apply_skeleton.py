#!/usr/bin/env python3
"""将 skeleton/ 复制到目标项目根目录，跳过已存在的文件（可选覆盖）。

用法:
    python scripts/apply_skeleton.py <target-project-root> [--overwrite]
"""
import argparse
import shutil
import sys
from pathlib import Path

SKELETON_DIR = Path(__file__).resolve().parent.parent / "skeleton"


def apply_skeleton(target: Path, *, overwrite: bool = False) -> None:
    if not SKELETON_DIR.is_dir():
        print(f"❌ skeleton 目录不存在: {SKELETON_DIR}", file=sys.stderr)
        sys.exit(1)

    target.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    for src_path in sorted(SKELETON_DIR.rglob("*")):
        # 跳过 __pycache__ 和 .pyc
        if "__pycache__" in src_path.parts or src_path.suffix == ".pyc":
            continue

        rel = src_path.relative_to(SKELETON_DIR)
        dst_path = target / rel

        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            continue

        if dst_path.exists() and not overwrite:
            print(f"  ⏭️  跳过 (已存在): {rel}")
            skipped += 1
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f"  ✅ 复制: {rel}")
        copied += 1

    print(f"\n完成: 复制 {copied} 文件, 跳过 {skipped} 文件")


def main() -> None:
    parser = argparse.ArgumentParser(description="将 Koi skeleton 应用到目标项目")
    parser.add_argument("target", type=Path, help="目标项目根目录")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的文件")
    args = parser.parse_args()
    apply_skeleton(args.target, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
