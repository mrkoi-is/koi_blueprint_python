# Bootstrap Checklist

## 1. 启动前确认

- 阅读 `README.md` 与 `docs/architecture.md`
- 确认目标项目采用 Koi 当前 Python 版本线
- 确认仓库初始化方式：新仓库 / 现有仓库增量接入
- 确认是否需要保留已有 CI、Docker、License、Git 历史

## 2. 骨架落地

- 使用 `scripts/apply_skeleton.py <target-project-root>` 复制 `skeleton/`
- 保留 `pyproject.toml`、`app/`、`tests/`、`Dockerfile`、`.env.example`、CI 基线
- 如果目标仓库已有同名文件，优先做差异合并，不要盲目覆盖

## 3. 启动后核对

至少确认以下文件存在且语义正确：
- `pyproject.toml`
- `app/main.py`
- `app/config.py`
- `app/core/`
- `tests/test_health.py`
- `.env.example`
- `Dockerfile`
- `.github/workflows/`

## 4. 基线验证

- 运行依赖同步命令
- 执行 Ruff、pyright、pytest
- 确认 `/health` 对应测试通过
- 确认应用能够本地启动

## 5. 完成标准

- 新项目具备最小可运行结构
- 质量门禁可执行
- Docker / CI 资产与应用结构一致
- 后续只需在骨架上增量增加业务模块
