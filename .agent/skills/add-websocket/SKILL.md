---
name: add-websocket
description: Add WebSocket support to a Koi-standard Python service. Use when implementing real-time communication such as chat, live notifications, device status streaming, or collaborative editing.
---

> 适配 `docs/architecture.md` v4.0

## Workflow

1. 在领域模块创建 `ws_router.py`:
   ```python
   from fastapi import APIRouter, WebSocket, WebSocketDisconnect
   import structlog

   router = APIRouter()
   logger = structlog.get_logger()

   class ConnectionManager:
       def __init__(self):
           self.active: list[WebSocket] = []

       async def connect(self, ws: WebSocket):
           await ws.accept()
           self.active.append(ws)

       def disconnect(self, ws: WebSocket):
           self.active.remove(ws)

       async def broadcast(self, message: str):
           for ws in self.active:
               await ws.send_text(message)

   manager = ConnectionManager()

   @router.websocket("/ws")
   async def websocket_endpoint(ws: WebSocket):
       await manager.connect(ws)
       try:
           while True:
               data = await ws.receive_text()
               await manager.broadcast(data)
       except WebSocketDisconnect:
           manager.disconnect(ws)
   ```

2. 在 `app/main.py` 注册: `app.include_router(ws_router)`
3. 注意: WebSocket 路由**必须**使用 `async def`
4. 认证: 通过查询参数传递 token `ws://host/ws?token=xxx`

## 测试

```python
from fastapi.testclient import TestClient

def test_websocket(client):
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert data == "hello"
```
