# minimal-service

最小结构样例。

用途：

- 展示 blueprint 复制到新项目后的最低可用形态
- 作为 `/health`、FastAPI `TestClient`、基础项目结构的参考

> 该目录是示例代码片段，不是独立打包单元；实际运行请以复制后的项目根目录为准。

运行方式：

```bash
uv sync --all-groups
uv run pytest
uv run uvicorn app.main:app --reload
```
