---
name: server-init
description: Scaffold a new Koi-standard Python service from the koi_blueprint_python repository. Use when creating a new Python/FastAPI backend, bootstrapping a fresh repository, copying the standard skeleton, installing baseline dependencies, and verifying /health and initial tests.
---

> 适配 `docs/architecture.md` v4.0

Use `scripts/apply_skeleton.py` to copy `skeleton/` into the target project root.

Workflow:
1. Read `docs/architecture.md`, especially Python version policy and bootstrap guidance.
2. Run `uv init --python <preferred-version> <project-name>`.
3. Run `scripts/apply_skeleton.py <target-project-root>`.
4. Sync dependencies with `uv sync --all-groups` or equivalent `uv add` commands.
5. Run `uv run ruff check .`, `uv run pyright`, and `uv run pytest`.
6. Confirm `tests/test_health.py` passes.

Load `references/bootstrap-checklist.md` when you need the full checklist.
