# Versioning Checklist

## 1. 路由入口

- `app/main.py` 是否定义统一 `api_prefix`
- 是否通过 `include_router(..., prefix=api_prefix)` 注册
- 是否避免在各 router 内重复硬编码主版本前缀

## 2. 版本策略

- 是否使用 URL path versioning（如 `/api/v1`）
- 新版本是否通过独立 router / 模块注册
- 是否存在清晰的弃用说明

## 3. 文档与测试

- OpenAPI 文档是否反映当前版本
- 测试是否覆盖 `v1` / `v2` 路由差异
- README / examples / docs 是否同步更新

## 4. 反模式

- 在一个 handler 中混杂多个版本逻辑
- router 内直接写死 `/api/v1/...`
- 新版本上线但旧版本没有测试或弃用计划
