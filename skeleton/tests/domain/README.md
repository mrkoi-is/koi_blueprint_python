# 领域测试 / Domain Tests
#
# 在此添加领域模块的单元测试。
# Place domain module unit tests here.
#
# 使用 MemoryRepository 替代数据库依赖：
# Use MemoryRepository to avoid database dependencies:
#
#   from app.core.repository import MemoryRepository
#
#   class MemoryDeviceRepo(MemoryRepository[Device]):
#       pass
#
#   def test_create_device():
#       repo = MemoryDeviceRepo()
#       service = DeviceService(repo)
#       service.create(name="sensor-01")
#       assert repo.count() == 1
