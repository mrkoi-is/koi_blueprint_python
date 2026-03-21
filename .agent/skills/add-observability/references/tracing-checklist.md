# Tracing Checklist

## 何时值得接 tracing

- 存在跨服务调用
- 存在慢请求但仅靠日志难定位
- 需要观察数据库 / HTTP client / 消息队列耗时
- 需要把用户请求贯穿到 worker 或外部服务链路

## 推荐接入顺序

1. 设定统一 `service.name`、`service.version`、`deployment.environment`。
2. 初始化 `TracerProvider` 与 exporter。
3. 为 FastAPI、HTTP client、数据库驱动按需加 instrumentation。
4. 对关键业务操作补业务 span，不要在所有函数上过度埋点。
5. 根据环境配置采样率，本地 / staging / production 可不同。

## 设计约束

- 未明确收益前，不要把 tracing 作为新项目默认强制依赖。
- exporter 地址、认证、采样率都应走配置。
- 注意敏感信息脱敏，不要把 token、密码、PII 写进 span attribute。
- worker / queue 场景如需串联 trace，上下文传播策略要明确。

## 最小验证

- 本地可在 Jaeger / OTLP 后端看到 FastAPI 请求 span
- 核心外部调用具备子 span
- 异常请求能看到 error status
- 关闭 tracing 配置后，服务仍可正常启动
