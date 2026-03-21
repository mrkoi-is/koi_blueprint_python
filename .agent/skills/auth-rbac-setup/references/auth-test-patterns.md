# Auth Test Patterns

## Unit Tests

优先覆盖：
- `get_current_user(None)`
- valid token
- invalid token
- expired token
- `get_optional_user(None)`
- `require_role` allow / deny

## API Tests

适用场景：
- 路由确实挂载了 auth 依赖
- `401` 与 `403` 返回符合预期
- 错误响应结构包含 `code` / `message` / `path`

## 注意

- 使用测试专用 secret，避免过短密钥警告
- 不要在测试里复制业务 token 生成逻辑过多次，抽辅助函数
