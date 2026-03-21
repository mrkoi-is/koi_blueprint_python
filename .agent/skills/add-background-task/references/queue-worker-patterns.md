# Queue Worker Patterns

## Celery / ARQ 共同检查项

- 独立 worker 入口
- broker / result backend 配置
- 幂等 task 设计
- 明确超时、重试、退避策略
- 本地 compose 与生产部署口径一致
- 失败任务可追踪、可报警

## Celery 模式

适合：
- 定时任务较多
- 需要成熟生态与管理工具
- 需要多队列、多 worker 池、复杂重试策略

推荐文件结构：
- `app/worker.py`：Celery app 初始化
- `app/domain/<module>/tasks.py`：任务定义
- `docker-compose.yml`：`api` / `worker` / `beat` / `redis`

## ARQ 模式

适合：
- 已有 async 栈
- Redis 已经是基础依赖
- 任务编排复杂度中等

推荐文件结构：
- `app/worker.py`：ARQ WorkerSettings
- `app/domain/<module>/tasks.py`：异步任务函数
- `app/core/dependencies.py`：为 worker 单独准备依赖工厂

## 设计约束

- task 中只放“可重放”的业务步骤，不要耦合 HTTP 层对象。
- 与数据库交互时，worker 进程要自己管理 Session / UoW 生命周期。
- 对外部系统调用要有超时、重试、熔断或补偿策略。
- 若任务结果需要给用户查询，提供状态存储与查询接口，不要只靠日志排查。
