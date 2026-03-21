# minimal-service

最小可运行金样例。

用途：

- 展示 blueprint 复制到新项目后的最低可用形态
- 作为 `/health`、FastAPI `TestClient`、基础项目结构的参考

运行方式：

```bash
uv sync --all-groups
uv run pytest
uv run uvicorn app.main:app --reload
```
