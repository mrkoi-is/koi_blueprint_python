# Migration Strategies

## 场景 1：首次引入版本

适合：当前还没有 `/api/v1` 前缀。

建议：
- 在 `app/main.py` 增加统一 `api_prefix = "/api/v1"`
- 通过 `include_router(..., prefix=api_prefix)` 注入
- 同步更新测试与示例

## 场景 2：新增 v2 并保留 v1

建议：
- 为新版本新增独立 router 或模块
- 在 `main.py` 中明确注册 `v1` 与 `v2`
- 对 breaking changes 保持旧版本行为不变

## 场景 3：弃用旧版本

建议：
- 保留旧版本一段时间
- 文档标记 deprecated
- 测试覆盖旧版本直到下线
- 在变更记录中声明移除时间点
