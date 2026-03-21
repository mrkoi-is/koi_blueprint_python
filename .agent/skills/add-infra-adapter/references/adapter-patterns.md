# Infra Adapter Pattern

## 1. 推荐结构

每个基础设施适配器通常包含：
- `abstract.py`：抽象接口 / port
- `<implementation>.py`：真实实现
- `memory.py`：测试替身或本地 fallback
- `__init__.py`：导出公共接口
- `app/core/dependencies.py`：依赖接线

## 2. 职责边界

- domain / service 层只依赖 `abstract.py` 中的接口
- 真实 SDK 调用集中在 `app/infra/` 下
- 配置、鉴权、超时、重试由配置层与适配器层统一处理

## 3. 测试模式

- 单元测试优先使用 `memory.py`
- 真实第三方联调测试应独立，不要污染纯业务测试
- 替身实现应尽量贴近真实契约，而不只是“能过测试”

## 4. 接线要点

- 在 `app/core/dependencies.py` 暴露 provider
- 按环境切换真实实现与测试替身
- 对 SDK 异常进行语义化封装，避免外泄到 router

## 5. 设计约束

- 不要在 service 中直接创建 SDK client
- 不要把第三方返回结构直接渗透到领域层
- 不要让测试替身与真实契约长期漂移
