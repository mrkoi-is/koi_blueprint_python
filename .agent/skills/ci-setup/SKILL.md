---
name: ci-setup
description: Configure the standard Koi CI pipeline for a Python service. Use when creating or updating GitHub Actions workflows for Ruff, pyright, pytest, security scanning, Docker builds, optional image publishing, and repository quality gates.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 新建或调整 GitHub Actions CI 流水线
- 接入 Ruff、pyright、pytest、安全扫描与镜像构建
- 区分 CI 与 CD 职责，避免把发布逻辑混进基础校验
- 审核仓库门禁是否达到 Koi 标准

## Workflow

1. Read `docs/architecture.md` 中与工具链、测试、Docker、安全扫描相关的章节。
2. Use `assets/ci.template.yml` as the starting point.
3. Confirm the target repository already aligns on `uv`, Ruff, pyright, pytest, and any required service dependencies.
4. Add optional registry login, image push, or environment deploy only when the target project explicitly needs them.
5. Keep branch protection and required checks aligned with the workflow job names.
6. Validate the workflow syntax and, when practical, run the same commands locally before finalizing.

## CI Rules

- 先保证 lint / type / test / security 的基础门禁，再谈发布优化。
- CI 与 CD 尽量拆分，避免一次 workflow 既做质量校验又直接上线。
- 缓存策略要服务于稳定性，不要为了省几秒牺牲可重复性。
- 所有门禁命令应能在本地或容器内复现，而不是只在 GitHub 上神秘通过。

Load `references/ci-options.md` for optional workflow variants.
