---
name: server-init
description: Scaffold a new Koi-standard Python service from the koi_blueprint_python repository. Use when creating a new FastAPI backend, bootstrapping a repository from `skeleton/`, syncing baseline dependencies, and verifying the initial health endpoint, lint, type checks, and tests.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 初始化一个新的 Python / FastAPI 服务项目
- 从 `skeleton/` 拷贝标准骨架并完成首轮接线
- 对齐基础依赖、目录结构、`/health` 与测试基线
- 审核一个新仓库是否按 Koi 标准完成 bootstrap

## Workflow

1. Read `README.md` and `docs/architecture.md`, especially Python version policy and bootstrap guidance.
2. Run `scripts/apply_skeleton.py <target-project-root>` after preparing the target repository.
   - 脚本默认同时复制骨架代码和 AI 工具链资产（`.agent/`, `.cursor/`, `AGENTS.md`, `docs/`）。
   - 如果不需要 AI 资产，使用 `--no-ai-assets` 跳过。
3. Confirm the generated project includes `pyproject.toml`, `app/`, `tests/`, Docker assets, and CI baseline files.
4. Confirm AI tooling assets are present: `AGENTS.md`, `.agent/skills/`, `.cursor/rules/`, `docs/ai-quickstart.md`, `docs/architecture.md`.
5. Sync dependencies with `uv sync --all-groups` or the equivalent `uv add` flow when the target project needs incremental adoption.
6. Validate the baseline with `uv run ruff check .`, `uv run pyright`, and `uv run pytest`.
7. Confirm `tests/test_health.py` and the default application startup path both work.

## Bootstrap Principles

- 优先复用 `skeleton/` 与根级脚本，不要手写一套近似但漂移的起步模板。
- 初始化阶段先保证“可运行、可测试、可检查”，再加业务代码。
- 新项目必须对齐 Python 版本、工具链、目录结构与配置入口。
- 新项目必须包含 AI 工具链资产，使任何 AI 工具都能正确路由到 Koi 标准 Skill。
- 生成后若需定制，保持在 Koi 基线之上增量调整，而不是回退到自由发挥。

Load `references/bootstrap-checklist.md` when you need the full bootstrap checklist.
