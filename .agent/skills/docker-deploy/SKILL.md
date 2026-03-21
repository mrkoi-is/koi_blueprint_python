---
name: docker-deploy
description: Prepare Docker deployment assets for a Koi-standard Python service. Use when adding or updating Dockerfile, docker-compose files, `.dockerignore`, runtime env wiring, image verification steps, and local container-based smoke tests.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 为服务补 Dockerfile、compose、`.dockerignore` 等部署资产
- 校准镜像构建、环境变量注入与本地容器联调
- 给项目增加容器化 smoke test 或基础部署验证
- 审核当前 Docker 资产是否符合 Koi 标准

## Workflow

1. Read `docs/architecture.md` 中与 Docker、配置、健康检查、部署相关的章节。
2. Confirm the project root already contains the standard `Dockerfile` or decide how far it diverges from Koi baseline.
3. Use `assets/docker-compose.template.yml` as the default local composition template.
4. Adapt compose services, env vars, volumes, and dependent services to the target project.
5. Add or update `.dockerignore`, then verify with `docker compose build` and `docker compose up -d`.
6. Confirm `/health` and any required readiness endpoints respond as expected inside the containerized setup.

## Deployment Rules

- 镜像构建必须可重复，不要依赖未锁定或只在本机存在的文件。
- Docker 资产优先服务本地验证与部署一致性，不要堆无用 compose 变体。
- 健康检查、配置文件、依赖服务端口要与应用实际行为一致。
- 若项目已有平台化部署方案，compose 资产应作为本地联调模板，而非强行替代生产编排。

Load `references/deploy-checklist.md` for the deployment checklist.
