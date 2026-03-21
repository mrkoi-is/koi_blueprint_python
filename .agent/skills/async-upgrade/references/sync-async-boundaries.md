# Sync / Async Boundaries

## 推荐

- 普通 CRUD、低并发 I/O：保留同步 `def`
- WebSocket、流式接口、大量外部 API 并发：使用 `async def`

## 反模式

- `async def` 中继续使用同步 `Session`
- `async def` 中执行阻塞 SDK / `time.sleep`
- 只有 router 异步，repository 仍同步阻塞

## 改造顺序

1. 驱动与 session factory
2. UoW
3. repository
4. service
5. router
6. tests
