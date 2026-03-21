# Deploy Readiness

## 上线前最低检查项

- 所有质量门禁通过
- 镜像可构建
- 环境变量已替换为生产值
- 数据库迁移脚本可执行
- 健康检查端点可访问
- 日志输出格式满足排障需求
- 至少具备一个 metrics 或 tracing 接入点

## 常见阻塞点

- `README` / `uv.lock` / `.dockerignore` 缺失
- 容器里依赖安装方式不稳定
- 仍使用示例密钥
- 只有 `/health` 没有数据库 / Redis readiness
- CI 只跑 lint 不跑测试和镜像构建
