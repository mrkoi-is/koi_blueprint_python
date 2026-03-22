# koi_blueprint_python

[![CI](https://github.com/mrkoi-is/koi_blueprint_python/actions/workflows/ci.yml/badge.svg)](https://github.com/mrkoi-is/koi_blueprint_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mrkoi-is/koi_blueprint_python/graph/badge.svg)](https://codecov.io/gh/mrkoi-is/koi_blueprint_python)
![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue)
[![License: MIT](https://img.shields.io/github/license/mrkoi-is/koi_blueprint_python)](LICENSE)

[中文文档](README_ZH.md)

An AI-Agent-oriented Python server architecture blueprint repository.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/mrkoi-is/koi_blueprint_python.git
cd koi_blueprint_python/skeleton

# 2. Install deps
uv sync --all-groups

# 3. Lint + Type check + Test
uv run ruff check .
uv run pyright
uv run pytest
```

> See `docs/ai-quickstart.md` for the shortest AI onboarding path.

---

## What's Inside

This repository enables AI agents to generate Koi-standard Python server projects consistently. It provides:

- `docs/architecture.md` — Universal architecture standard (1000+ lines covering toolchain → patterns → constraints → observability → API versioning)
- `skeleton/` — Minimal runnable skeleton (complete core modules, tests, CI, Docker)
- `examples/` — Minimal service, domain module, and async service examples
- `.agent/skills/` — 16 installable AI Agent Skills (maintained against architecture v4.0)

## Usage Modes

### Mode 1: Knowledge Base

Have the AI read:

1. `docs/ai-quickstart.md`
2. `README.md`
3. `docs/architecture.md`
4. `skeleton/`
5. `examples/`

For environments that cannot auto-discover Skills.

### Mode 2: Native Tool Discovery (Recommended)

| Tool | Discovery |
|------|-----------|
| **Google Antigravity** | Workspace-level Skills at `.agent/skills/`; `SKILL.md` `description` used for agent routing. |
| **OpenAI Codex (CLI/IDE)** | Root `AGENTS.md` describes Skill index and required reading; optionally symlink `.agent/skills/*` to `$CODEX_HOME/skills/`. |
| **Cursor** | `.cursor/rules/koi-agent-skills.mdc` (`alwaysApply`) + root `AGENTS.md`, prompts reading `.agent/skills/<id>/SKILL.md` on task match. |
| **Other Agents** | Read `AGENTS.md`, then open the corresponding `SKILL.md` as needed. |

For environments that cannot auto-index directories, use **Mode 1** and manually `@` reference `SKILL.md`.

## Directory Guide

- `docs/ai-quickstart.md` — Shortest AI onboarding path
- `docs/how-other-ai-use-this-project.md` — Integration guide for AI tools
- `AGENTS.md` — Cross-tool Agent entry point
- `docs/agent-skill-rule-discovery.md` — Skill / Rule discovery per platform
- `docs/architecture.md` — Koi Python server architecture standard (v4.0)
- `skeleton/` — Minimal runnable project skeleton
- `examples/minimal-service/` — Minimal structure example
- `examples/device/` — Full domain layer example
- `examples/async-service/` — Full async path example
- `.agent/skills/` — 16 Skill source directories
- `.agent/skills/index.yaml` — Machine-readable intent → skill routing index
- `scripts/` — Root-level scaffold scripts

## Tech Stack

- Python **3.13+** (only certified version)
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (Mapped)
- uv + Ruff + pyright (Astral toolchain)
- structlog + Prometheus (observability)
- Testcontainers + pytest
- Bandit + pip-audit (security scanning)

## Skills

| Skill | Purpose |
|---|---|
| `server-init` | Scaffold new project from skeleton |
| `add-domain-module` | Scaffold domain module |
| `add-infra-adapter` | Scaffold infra adapter |
| `alembic-migration` | Database migration management |
| `ci-setup` | CI/CD pipeline configuration |
| `docker-deploy` | Docker deployment assets |
| `add-background-task` | Background tasks (Celery/ARQ) |
| `add-websocket` | WebSocket support |
| `add-observability` | Prometheus + OpenTelemetry |
| `architecture-review` | Koi architecture review |
| `testing-scaffold` | Test scaffolding |
| `auth-rbac-setup` | JWT auth + RBAC |
| `production-hardening` | Production readiness |
| `async-upgrade` | Async architecture upgrade |
| `api-versioning` | API versioning & migration |
| `rate-limit-setup` | Rate limiting + 429 testing |

## Development

1. Maintain `docs/architecture.md` first
2. Then `skeleton/`, ensure `pytest` passes
3. Then `examples/`
4. Finally `.agent/skills/` scripts, templates, and references

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting policy.

## License

[MIT](LICENSE) © mrkoi
