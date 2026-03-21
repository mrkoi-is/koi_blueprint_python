---
name: api-versioning
description: Add or review API versioning in a Koi-standard Python service. Use when introducing versioned route prefixes such as /api/v1 and /api/v2, evolving contracts without breaking clients, deprecating endpoints, or auditing router registration and migration strategy for FastAPI services.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 引入 `v1` / `v2` API 路由版本
- 调整 `api_prefix` 与 router 注册方式
- 做接口平滑升级与兼容迁移
- 审查当前版本策略是否合理
- 输出版本演进计划或弃用策略

## Workflow

1. Read `docs/architecture.md` 中的 API 版本管理相关章节。
2. Inspect the target project's:
   - `app/main.py`
   - `app/domain/*/router.py`
   - OpenAPI / docs exposure strategy
   - tests for versioned endpoints
3. Run `scripts/inspect_versioning_surface.py <target-root>` to collect versioning signals.
4. Compare current implementation against `references/versioning-checklist.md`.
5. Decide the required change type:
   - 初次引入版本前缀
   - 新增 `v2` 并保留 `v1`
   - 弃用旧版本
   - 统一文档与测试
6. Use `references/migration-strategies.md` to choose rollout strategy.
7. If the user asks for a rollout plan, use `assets/versioning-plan-template.md`.

## Versioning Principles

- 默认用 URL prefix 版本化，例如 `/api/v1`。
- 新版本优先通过新增 router 或新增 prefix 落地，不在单一路由里堆大量 `if version` 分支。
- 对外行为变更时，优先保留旧版本并显式声明弃用期。
- 文档、测试、示例必须与版本策略同步更新。

Load `references/versioning-checklist.md` and `references/migration-strategies.md` as needed.
