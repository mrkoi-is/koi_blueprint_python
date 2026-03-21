---
name: add-infra-adapter
description: Scaffold a new Koi-style infrastructure adapter under `app/infra/`. Use when integrating Redis, object storage, MQTT, mail, or another third-party service and you need abstract interfaces, concrete implementations, testing doubles, and dependency wiring.
---

> 适配 `docs/architecture.md` v4.0

Use `scripts/scaffold_adapter.py <project-root> <adapter-name> <implementation-name>` for deterministic scaffolding.

After scaffolding:
1. Add the external SDK dependency.
2. Wire the dependency provider in `app/core/dependencies.py`.
3. Add or update tests that use the memory double.
4. Run Ruff and pyright.

Load `references/adapter-patterns.md` when you need the expected file breakdown.
