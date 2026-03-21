---
name: production-hardening
description: Harden a Koi-standard Python service for production readiness. Use when improving Docker images, environment safety, health/readiness endpoints, metrics, logging, security scans, dependency pinning, CI quality gates, deployment assets, or operational checklists.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 把 Python/FastAPI 服务提升到生产可用状态
- 加强 Docker、CI、安全扫描、环境变量管理
- 补健康检查、就绪检查、metrics、日志统一
- 评估“是否可以上线”或“还差什么”

## Workflow

1. Read `docs/architecture.md`, especially tooling, Docker, observability, and security-related sections.
2. Inspect the target project's:
   - `pyproject.toml`
   - `Dockerfile`
   - `.dockerignore`
   - `.env.example`
   - `docker-compose.yml`
   - `.github/workflows/`
   - `app/main.py`
   - `app/core/logging.py`
   - `app/core/metrics.py`
3. Run `scripts/inspect_production_surface.py <target-root>` to collect readiness signals.
4. Compare the project against `references/hardening-checklist.md`.
5. Group changes into:
   - runtime safety
   - build reproducibility
   - CI quality gates
   - observability
   - deployment readiness
6. Prefer minimal, verifiable hardening changes over broad refactors.
7. If the user asks for a report or rollout plan, use `assets/hardening-report-template.md`.

## Hardening Principles

- 优先补“会导致上线失败或事故”的缺口。
- 优先让构建、测试、镜像、配置可重复。
- 优先让日志、健康检查、metrics 可观察。
- 对已有 skeleton 项目，优先复用 Koi 现有 Docker / CI / core 资产。

Load `references/hardening-checklist.md` and `references/deploy-readiness.md` as needed.
