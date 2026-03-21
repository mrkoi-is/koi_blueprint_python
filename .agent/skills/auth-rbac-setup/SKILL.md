---
name: auth-rbac-setup
description: Add or review JWT auth and role-based access control in a Koi-standard Python service. Use when wiring get_current_user, get_optional_user, require_role, auth-related exception handling, protected routes, or auth unit tests.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 接入 JWT 鉴权
- 增加角色权限控制
- 修复 401 / 403 语义不一致
- 给路由加登录态或角色限制
- 补 auth 相关单测

## Workflow

1. Read `app/core/auth.py`, `app/core/exceptions.py`, and `app/core/exception_handlers.py`.
2. Read `references/auth-checklist.md` for the baseline rules.
3. Run `scripts/inspect_auth_surface.py <target-root>` to gather current auth signals.
4. Ensure the project provides:
   - `get_current_user`
   - `get_optional_user`
   - `require_role(*roles)`
   - `AuthenticationError` / `ForbiddenError`
5. For protected endpoints:
   - use `Depends(get_current_user)` for login requirement
   - use `Depends(require_role(...))` for RBAC
6. Add or update unit tests using `references/auth-test-patterns.md`.
7. Validate status semantics:
   - missing/invalid token → 401
   - insufficient role → 403

## Constraints

- 不要把业务权限逻辑散落到 router if/else 中。
- 不要吞掉无效 token 的错误原因，除非接口明确允许匿名访问。
- 默认以 Koi 当前内建 JWT 基线为准，不在此 Skill 中扩展到完整 OAuth2 / OIDC Provider 流程。

Load `references/auth-checklist.md` and `references/auth-test-patterns.md` as needed.
