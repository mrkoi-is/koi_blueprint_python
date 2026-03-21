# WebSocket Auth and Testing

## 鉴权策略

常见 token 传递方式：
- Query parameter
- Header / Cookie（取决于客户端能力）
- 首条握手消息（仅在协议设计明确时使用）

推荐约束：
- 与 HTTP 鉴权共用同一套 token 解析逻辑
- 认证失败尽早关闭连接
- 角色不足时返回清晰错误并断开或拒绝订阅

## 测试清单

至少覆盖：
- 成功连接
- 首次消息收发
- 断开后连接管理器清理
- 无 token / token 无效
- 权限不足

## 最小测试模式

```python
with client.websocket_connect("/ws?token=test-token") as ws:
    ws.send_text('{"type": "ping"}')
    message = ws.receive_text()
    assert message
```

## 易错点

- 在同步测试里调用需要事件循环的外部依赖
- 把数据库 Session 或 Request 直接塞进连接管理器
- 没有处理 `WebSocketDisconnect`
- 多实例部署仍使用单例内存广播而未说明限制
