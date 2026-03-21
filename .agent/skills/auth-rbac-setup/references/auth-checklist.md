# Auth Checklist

## 1. 核心函数

- `get_current_user`
- `get_optional_user`
- `require_role(*roles)`

## 2. 状态语义

- 缺失凭证 → 401
- 无效 Token → 401
- 权限不足 → 403

## 3. 异常体系

- `AuthenticationError`
- `ForbiddenError`
- `WWW-Authenticate: Bearer`

## 4. Router 用法

- 登录保护：`Depends(get_current_user)`
- 角色保护：`Depends(require_role("admin"))`
- 匿名可选：`Depends(get_optional_user)`

## 5. 最小验证项

- 有效 token 可通过
- 缺失 token 抛 401
- 无效 token 抛 401
- 非法角色抛 403
