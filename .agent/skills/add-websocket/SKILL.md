---
name: add-websocket
description: Add WebSocket support to a Koi-standard Python service. Use when implementing chat, live notifications, device status streaming, collaborative sessions, connection managers, authentication for websocket endpoints, and real-time integration tests.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 为服务增加实时通信、推送、状态订阅或双向会话能力
- 实现 `ConnectionManager`、房间广播、在线连接管理
- 给 WebSocket 路由补鉴权、错误处理与测试
- 审核 sync / async 边界、消息格式与实时链路设计是否合理

## Workflow

1. Read `docs/architecture.md` 中与 FastAPI、异步边界、WebSocket 场景相关的章节。
2. Inspect the target project's:
   - `app/main.py`
   - `app/core/auth.py`
   - `app/core/dependencies.py`
   - target domain routers / services
   - tests for real-time flows
3. Run `scripts/inspect_websocket_surface.py <target-root>` to inspect current router, auth, and real-time testing signals.
4. Use `references/websocket-patterns.md` to decide route shape, connection manager scope, and broadcast strategy.
5. Use `references/websocket-auth-and-testing.md` to handle token passing, permission checks, disconnect behavior, and test layout.
6. Keep WebSocket handlers `async def`, and keep business rules inside services or dedicated managers instead of embedding everything in the router.
7. Decide whether the connection scope is per-process, per-room, or needs an external pub/sub bridge.
8. Add or update tests for connect, message round-trip, auth failure, and disconnect cleanup.

## WebSocket Principles

- WebSocket 适合实时链路，不要拿它替代普通 CRUD HTTP 接口。
- 单进程内存连接管理器只适用于单实例场景；多实例广播需要 Redis / MQ / pub-sub。
- 鉴权必须与 HTTP 口径一致，401 / 403 语义要清晰。
- 消息 schema、心跳、断线清理与背压策略要在设计阶段说明，而不是上线后补救。

Load `references/websocket-patterns.md` and `references/websocket-auth-and-testing.md` as needed.
