# WebSocket Patterns

## 推荐结构

- `app/domain/<module>/ws_router.py`：WebSocket 路由
- `app/domain/<module>/service.py`：业务处理逻辑
- `app/domain/<module>/manager.py`：连接管理、房间广播、订阅表
- `app/core/auth.py`：复用 token 解析与用户识别逻辑

## 单实例模式

适合：
- 开发环境
- 单实例部署
- 简单广播或状态推送

核心约束：
- 连接管理器只保存当前进程内连接
- 广播只对本进程连接有效
- 重启即丢连接状态

## 多实例模式

适合：
- 多副本部署
- 需要跨实例广播
- 需要与后台任务联动推送

推荐做法：
- WebSocket 只维护连接
- 广播事件走 Redis pub/sub、消息队列或专用网关
- 不要试图用进程内列表解决跨实例问题

## 代码组织原则

- router 处理接入、鉴权、序列化、异常边界
- manager 管理连接生命周期
- service 处理消息语义与领域行为
- schema 明确入站 / 出站消息格式
