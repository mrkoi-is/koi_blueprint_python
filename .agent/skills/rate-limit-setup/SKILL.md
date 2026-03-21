---
name: rate-limit-setup
description: Add or review rate limiting in a Koi-standard Python service. Use when protecting public or high-risk endpoints, introducing slowapi or equivalent middleware, configuring per-route throttling, exempting health/metrics endpoints, or adding tests for 429 behavior in FastAPI services.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 接入接口限流
- 为登录、验证码、公开接口、Webhook 等高风险入口设置节流
- 审查现有限流方案是否合理
- 补 429 测试与错误处理

## Workflow

1. Read `docs/architecture.md` 中速率限制相关章节。
2. Inspect the target project's:
   - `app/main.py`
   - middleware / dependencies setup
   - public routers
   - auth-related routes
   - tests for 429 behavior
3. Run `scripts/inspect_rate_limit_surface.py <target-root>` to collect rate-limit signals.
4. Compare the project against `references/rate-limit-checklist.md`.
5. Determine the correct scope:
   - 全局限流
   - 按路由限流
   - 仅对高风险接口限流
6. Use `references/route-priority-guide.md` to choose which endpoints should be stricter.
7. If the user asks for an implementation plan, use `assets/rate-limit-plan-template.md`.

## Rate Limit Principles

- 优先保护公开、高频、容易被滥用的接口。
- `/health`、`/metrics` 等基础设施端点通常应豁免或单独策略处理。
- 限流策略必须配套清晰的 429 响应与测试。
- 不要把所有接口一刀切为同一个限额。

Load `references/rate-limit-checklist.md` and `references/route-priority-guide.md` as needed.
