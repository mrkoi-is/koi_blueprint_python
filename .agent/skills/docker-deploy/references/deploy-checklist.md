# Deploy Checklist

## 1. 构建资产

- `Dockerfile` 存在且可构建
- `.dockerignore` 存在且排除了无关上下文
- 依赖安装方式稳定、可重复

## 2. 运行资产

- `docker-compose.yml` 或等效本地编排文件存在
- 应用、数据库、Redis 等依赖服务定义完整
- 环境变量通过 `.env` 或显式 env 注入
- 健康检查、端口、卷挂载与真实行为一致

## 3. 验证步骤

- `docker compose build` 成功
- `docker compose up -d` 成功
- `/health` 可访问
- 如有 `/ready` / `/metrics`，也应符合预期

## 4. 设计约束

- compose 优先服务本地联调与验证
- 生产环境如使用其他编排平台，不强行照搬 compose
- 不要依赖本机私有文件或未提交资产
