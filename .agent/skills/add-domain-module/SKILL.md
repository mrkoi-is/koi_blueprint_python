---
name: add-domain-module
description: Scaffold a new Koi-standard domain module inside an existing Python service. Use when adding a new business module under `app/domain/`, creating router/schema/model/service/repository files, wiring router registration, and generating matching test stubs.
---

> 适配 `docs/architecture.md` v4.0

Use `scripts/scaffold_domain.py <project-root> <module-name>` for deterministic scaffolding.

After scaffolding:
1. Review generated DTOs, repository interfaces, and service methods.
2. Register the router in `app/main.py` if the script could not insert it automatically.
3. Generate a database migration when models change.
4. Run Ruff, pyright, and pytest.

Load `references/domain-patterns.md` for the file-by-file pattern details.
