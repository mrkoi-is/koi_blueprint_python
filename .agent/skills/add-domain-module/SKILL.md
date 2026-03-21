---
name: add-domain-module
description: Scaffold a new Koi-standard domain module inside an existing Python service. Use when adding a business module under `app/domain/`, generating router/schema/model/service/repository files, wiring router registration, and creating aligned unit or integration test stubs.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 新增一个业务领域模块
- 生成 router / schema / model / service / repository 基础结构
- 自动注册路由并补测试骨架
- 审核现有领域模块是否符合 Koi 分层模式

## Workflow

1. Read `docs/architecture.md` 中与分层、DTO、Repository、UoW 相关的章节。
2. Run `scripts/scaffold_domain.py <project-root> <module-name>` for deterministic scaffolding.
3. Review generated DTOs, repository interfaces, service methods, and route registration.
4. If the module adds or changes ORM models, generate an Alembic migration.
5. Add or refine tests under the appropriate `tests/unit/` or `tests/integration/` path.
6. Validate with Ruff, pyright, and pytest.

## Domain Module Rules

- router 只处理 HTTP 边界，不在其中堆业务判断。
- service 只依赖抽象接口，不直接绑定 FastAPI 或第三方 SDK。
- repository / UoW 负责持久化边界，命名与方法粒度保持清晰稳定。
- 新模块的测试至少覆盖核心服务行为，不要留下永久占位测试。

Load `references/domain-patterns.md` for the file-by-file domain module pattern.
