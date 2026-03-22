#!/usr/bin/env python3
"""将 skeleton/ 和 AI 工具链资产复制到目标项目根目录，跳过已存在的文件（可选覆盖）。

用法:
    python scripts/apply_skeleton.py <target-project-root> [--overwrite] [--no-ai-assets]
"""
import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKELETON_DIR = REPO_ROOT / "skeleton"

# AI 工具链资产：需要复制到新项目以确保 AI 能正确路由和使用 Koi 标准
AI_ASSET_FILES = [
    "AGENTS.md",
]

AI_ASSET_DIRS = [
    ".agent",
    ".cursor",
]

# docs/ 中只复制 AI 和架构相关文档，跳过蓝图仓库自身的报告类文件
AI_ASSET_DOCS = [
    "docs/ai-quickstart.md",
    "docs/architecture.md",
    "docs/how-other-ai-use-this-project.md",
    "docs/agent-skill-rule-discovery.md",
]

# 复制时全局跳过的文件和目录名
SKIP_NAMES = {"__pycache__", ".DS_Store"}
SKIP_SUFFIXES = {".pyc"}


def _should_skip(path: Path) -> bool:
    """判断是否应跳过此路径。"""
    return any(part in SKIP_NAMES for part in path.parts) or path.suffix in SKIP_SUFFIXES


def _copy_tree(
    src_base: Path,
    target: Path,
    *,
    overwrite: bool,
    label: str,
) -> tuple[int, int]:
    """递归复制 src_base 下所有文件到 target，返回 (copied, skipped)。"""
    copied = 0
    skipped = 0

    for src_path in sorted(src_base.rglob("*")):
        if _should_skip(src_path):
            continue

        rel = src_path.relative_to(src_base)
        dst_path = target / rel

        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            continue

        if dst_path.exists() and not overwrite:
            print(f"  ⏭️  跳过 (已存在): {rel}  [{label}]")
            skipped += 1
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f"  ✅ 复制: {rel}  [{label}]")
        copied += 1

    return copied, skipped


def _copy_single_file(
    src: Path,
    target: Path,
    rel_path: str,
    *,
    overwrite: bool,
    label: str,
) -> tuple[int, int]:
    """复制单个文件，返回 (copied, skipped)。"""
    dst = target / rel_path
    if dst.exists() and not overwrite:
        print(f"  ⏭️  跳过 (已存在): {rel_path}  [{label}]")
        return 0, 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  ✅ 复制: {rel_path}  [{label}]")
    return 1, 0


def apply_skeleton(
    target: Path,
    *,
    overwrite: bool = False,
    ai_assets: bool = True,
) -> None:
    if not SKELETON_DIR.is_dir():
        print(f"❌ skeleton 目录不存在: {SKELETON_DIR}", file=sys.stderr)
        sys.exit(1)

    target.mkdir(parents=True, exist_ok=True)

    total_copied = 0
    total_skipped = 0

    # ── 第 1 步：复制骨架代码 ──
    print("📦 复制骨架代码 (skeleton/)...")
    c, s = _copy_tree(SKELETON_DIR, target, overwrite=overwrite, label="skeleton")
    total_copied += c
    total_skipped += s

    # ── 第 2 步：复制 AI 工具链资产 ──
    if ai_assets:
        print("\n🤖 复制 AI 工具链资产...")

        # 单独的文件
        for rel_path in AI_ASSET_FILES:
            src = REPO_ROOT / rel_path
            if src.is_file():
                c, s = _copy_single_file(
                    src, target, rel_path, overwrite=overwrite, label="ai-assets"
                )
                total_copied += c
                total_skipped += s

        # 目录（递归）
        for dir_name in AI_ASSET_DIRS:
            src_dir = REPO_ROOT / dir_name
            if src_dir.is_dir():
                # 复制到 target/<dir_name>/
                for src_path in sorted(src_dir.rglob("*")):
                    if _should_skip(src_path):
                        continue
                    rel = Path(dir_name) / src_path.relative_to(src_dir)
                    dst_path = target / rel
                    if src_path.is_dir():
                        dst_path.mkdir(parents=True, exist_ok=True)
                        continue
                    if dst_path.exists() and not overwrite:
                        print(f"  ⏭️  跳过 (已存在): {rel}  [ai-assets]")
                        total_skipped += 1
                        continue
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print(f"  ✅ 复制: {rel}  [ai-assets]")
                    total_copied += 1

        # 指定的文档文件
        for rel_path in AI_ASSET_DOCS:
            src = REPO_ROOT / rel_path
            if src.is_file():
                c, s = _copy_single_file(
                    src, target, rel_path, overwrite=overwrite, label="ai-docs"
                )
                total_copied += c
                total_skipped += s
    else:
        print("\n⏩ 跳过 AI 工具链资产 (--no-ai-assets)")

    print(f"\n完成: 复制 {total_copied} 文件, 跳过 {total_skipped} 文件")


def main() -> None:
    parser = argparse.ArgumentParser(description="将 Koi skeleton 和 AI 工具链资产应用到目标项目")
    parser.add_argument("target", type=Path, help="目标项目根目录")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的文件")
    parser.add_argument(
        "--no-ai-assets",
        action="store_true",
        help="不复制 AI 工具链资产 (.agent/, .cursor/, AGENTS.md, docs/)",
    )
    args = parser.parse_args()
    apply_skeleton(args.target, overwrite=args.overwrite, ai_assets=not args.no_ai_assets)


if __name__ == "__main__":
    main()
