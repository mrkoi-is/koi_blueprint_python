---
name: testing-scaffold
description: Add or improve tests in a Koi-standard Python service. Use when scaffolding unit tests, integration tests, Testcontainers fixtures, MemoryRepository-based service tests, pytest markers, or coverage/quality checks for FastAPI services.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 为新模块补单元测试 / 集成测试
- 把占位测试改成可运行测试
- 接入 Testcontainers / pytest markers / coverage
- 审核测试目录是否符合 Koi 规范

## Workflow

1. Read the target module and identify whether it is:
   - pure service logic → prefer `tests/unit/`
   - API / DB wiring → prefer `tests/integration/`
2. Read `references/testing-patterns.md` for expected layouts.
3. Run `scripts/inspect_test_surface.py <target-root>` to inspect current test directories and fixtures.
4. Prefer:
   - `MemoryRepository` or fake UoW for service unit tests
   - `db_session` + Testcontainers for integration tests
5. When adding tests:
   - unit tests go under `tests/unit/`
   - integration tests go under `tests/integration/`
   - avoid placeholder assertions like `assert True`
6. If the project lacks pytest markers or coverage options, align `pyproject.toml` with Koi conventions.
7. Validate with `ruff`, `pytest`, and project-standard type checks when available.

## Testing Rules

- 单元测试优先测试业务行为，不测试框架细节。
- 集成测试优先验证 fixture、事务隔离和数据库连通性。
- 对 skeleton / generated module，优先消除永久 skip 与占位实现。

Load `references/testing-patterns.md` when deciding concrete layouts.
