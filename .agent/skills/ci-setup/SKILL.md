---
name: ci-setup
description: Configure the standard Koi CI pipeline for a Python service. Use when creating or updating GitHub Actions workflows for linting, type checking, tests, Docker builds, or optional publish and deploy stages.
---

Use `assets/ci.template.yml` as the starting point.

Workflow:
1. Confirm the repository uses `uv`, Ruff, pyright, and pytest.
2. Copy or adapt the CI template.
3. Add registry login and image push only when the target project requires it.
4. Keep deploy steps separate unless the project explicitly wants CD.
5. Validate the workflow locally when practical.

Load `references/ci-options.md` for optional variants.
