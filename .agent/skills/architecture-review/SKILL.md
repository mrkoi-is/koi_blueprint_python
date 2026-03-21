---
name: architecture-review
description: Audit a Python/FastAPI service against the Koi architecture standard. Use when reviewing project structure, dependency direction, lifecycle setup, configuration, exceptions, logging, auth, repository/UoW, testing, CI, or Docker alignment with docs/architecture.md.
---

> 适配 `docs/architecture.md` v4.0

Use this skill when the user asks to:
- 审核 / review 一个 Python 服务架构
- 对照 Koi 规范找差距
- 输出架构整改建议、优先级、迁移路线
- 评估 skeleton / examples / generated project 是否符合标准

## Workflow

1. Read `docs/architecture.md` and `README.md` to确认当前标准与仓库定位。
2. Inspect the target project's:
   - `pyproject.toml`
   - `app/main.py`
   - `app/config.py`
   - `app/core/`
   - `app/domain/`
   - `tests/`
   - `Dockerfile` / `docker-compose.yml`
   - `.github/workflows/`
3. Run `scripts/collect_review_inputs.py <target-root>` to快速收集结构信号。
4. Compare the project against the Koi checklist in `references/review-checklist.md`.
5. Group findings by:
   - 架构一致性
   - 工程化
   - 测试与质量
   - 安全与可观测性
6. Prioritize findings as `P0 / P1 / P2`.
7. If the user asks for a report, use `assets/review-report-template.md` as the output skeleton.

## Review Principles

- 优先识别“文档承诺”和“代码实现”之间的漂移。
- 优先找根因，不只列现象。
- 对 generated project，重点检查 Skill 输出是否真的符合 skeleton 与 architecture。
- 结论必须落到文件路径和具体改进项。

Load `references/review-checklist.md` for the detailed review dimensions.
