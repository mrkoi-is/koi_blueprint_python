---
name: docker-deploy
description: Prepare Docker deployment assets for a Koi-standard Python service. Use when adding or updating Dockerfile, docker-compose files, dockerignore rules, or local container-based verification steps.
---

> 适配 `docs/architecture.md` v4.0

Use `assets/docker-compose.template.yml` as the default local composition template.

Workflow:
1. Confirm the project root already contains the standard `Dockerfile`.
2. Adapt the compose template to the target project's env vars and service names.
3. Add `.dockerignore` when missing.
4. Verify with `docker compose build` and `docker compose up -d`.
5. Confirm `/health` responds as expected.

Load `references/deploy-checklist.md` for the deployment checklist.
