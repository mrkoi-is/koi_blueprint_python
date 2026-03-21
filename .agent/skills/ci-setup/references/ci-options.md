# CI Options

## 1. 基线流水线

建议默认包含：
- Ruff
- pyright
- pytest
- 安全扫描（如 `bandit`、`pip-audit`）
- Docker build smoke check（按项目需要）

## 2. 可选增强项

按项目需要增加：
- Python version matrix
- 缓存优化
- Docker registry login and push
- Workflow dispatch for manual releases
- 产物上传或测试报告汇总

## 3. CI / CD 拆分建议

- `ci.yml`：质量校验与构建验证
- `release.yml` / `deploy.yml`：发布与环境部署
- 不要把所有职责混进单一 workflow

## 4. 设计约束

- 所有 job 命令应可本地复现
- job 名称要稳定，便于分支保护配置
- 缓存是优化项，不是正确性的前提
