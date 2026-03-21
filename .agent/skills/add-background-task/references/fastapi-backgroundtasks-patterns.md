# FastAPI BackgroundTasks Patterns

## 适用前提

- 任务耗时短
- 失败后可接受人工补偿或重新触发
- 不需要跨进程存活
- 不需要任务结果后端

## 建议落点

- router 负责接收请求并调用 `background_tasks.add_task(...)`
- service 负责准备任务参数与业务规则
- 真正的 task 函数放在领域模块或 `app/core/tasks.py` 一类的可复用位置

## 推荐模式

```python
@router.post("/reports")
def export_report(background_tasks: BackgroundTasks, service: ReportService = Depends(...)):
    report_id = service.prepare_export(...)
    background_tasks.add_task(service.run_export, report_id)
    return {"status": "queued", "report_id": report_id}
```

## 注意事项

- 不要把数据库 Session 直接传到后台函数中。
- 背景函数内部应自行获取依赖，或只接收可序列化参数。
- 如果失败需要重试，说明它可能已经超出 `BackgroundTasks` 的适用范围。
- 长时间 CPU 密集任务不应留在 Web 进程里执行。
