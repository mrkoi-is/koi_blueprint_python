# Router 用法示例

- 登录保护：`Depends(get_current_user)`
- 角色保护：`Depends(require_role("admin"))`
- 匿名可选：`Depends(get_optional_user)`
