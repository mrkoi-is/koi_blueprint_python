---
name: add-infra-adapter
description: Scaffold a new Koi-style infrastructure adapter under `app/infra/`. Use when integrating Redis, object storage, MQTT, mail, third-party APIs, or another external service through abstract ports, concrete implementations, memory doubles, and dependency wiring.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 接入 Redis、对象存储、邮件、MQTT 或其他外部系统
- 生成抽象接口、真实实现、memory double 与依赖注入接线
- 统一外部依赖的测试替身与调用边界
- 审核现有 `app/infra/` 适配器是否符合 Koi 风格

## Workflow

1. Read `docs/architecture.md` 中与依赖倒置、基础设施适配器、配置、测试替身相关的章节。
2. Run `scripts/scaffold_adapter.py <project-root> <adapter-name> <implementation-name>` for deterministic scaffolding.
3. Add the required external SDK dependency and configuration fields.
4. Wire the provider in `app/core/dependencies.py` or equivalent composition root.
5. Add or update tests that use the generated memory double or fake implementation.
6. Validate with Ruff, pyright, and project-standard tests.

## Adapter Rules

- domain / service 层依赖抽象端口，不直接 import 第三方 SDK。
- 真实实现放在 `app/infra/`，测试替身与真实实现保持相同行为契约。
- 配置、超时、重试、认证信息都放在配置层，不要散落在业务代码。
- 对外部系统调用失败要有清晰错误语义，不要把 SDK 异常原样泄漏到 router。

Load `references/adapter-patterns.md` when you need the expected adapter file breakdown.
