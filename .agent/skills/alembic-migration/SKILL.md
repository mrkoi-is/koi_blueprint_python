---
name: alembic-migration
description: Generate, review, and apply Alembic migrations in a Koi-standard Python service. Use when ORM models change, when you need a new revision, when autogenerate must be reviewed manually, or when migration execution needs to be aligned with local and deployment workflows.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 在模型变更后生成新的数据库迁移
- 审核 Alembic 自动生成结果是否安全
- 执行本地升级 / 回滚验证
- 梳理迁移文件与部署流程的职责边界

## Workflow

1. Confirm `migrations/env.py` points at the correct settings and metadata source.
2. Run `uv run alembic revision --autogenerate -m "<message>"` when schema changes are ready.
3. Review the generated upgrade / downgrade logic manually against actual model intent.
4. Run `uv run alembic upgrade head` locally and verify the application still starts.
5. Keep production migration execution in deployment pipelines or controlled release steps.
6. When downgrades are unsafe, record that explicitly instead of pretending they are reversible.

## Migration Rules

- 自动生成只是起点，不是最终结果；每次 revision 都要人工复核。
- 迁移必须与真实 metadata 对齐，避免 `target_metadata = None` 一类伪接线。
- 破坏性变更要配套数据迁移、回填或灰度策略。
- 不要把生产数据库迁移隐藏在应用启动流程里偷偷执行。

Load `references/migration-checklist.md` for the detailed migration review checklist.
