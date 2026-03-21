"""设备路由 — 完整 DI 注入示例，对应 architecture.md §4.6。

Router 仅处理 HTTP 关注点（参数解析、状态码、DTO 转换），
业务逻辑全部委托给 Service。
"""

from fastapi import APIRouter, Depends, status

from app.core.pagination import PaginationParams
from app.core.responses import ApiResponse, PaginatedData

from .schemas import DeviceCreateSchema, DeviceResponse
from .service import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


def get_device_service() -> DeviceService:
    """DI 工厂 — 实际项目中从 app.core.dependencies 导入。

    此处为示例自包含实现；真实项目中应使用:
        from app.core.dependencies import get_device_service
    """
    raise NotImplementedError(
        "Replace with actual DI wiring: "
        "DeviceService(DeviceUnitOfWork(session_factory))"
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[DeviceResponse],
)
def create_device(
    payload: DeviceCreateSchema,
    service: DeviceService = Depends(get_device_service),
):
    device = service.register(payload.sn, payload.name)
    return ApiResponse(data=device)


@router.get("/", response_model=ApiResponse[PaginatedData[DeviceResponse]])
def list_devices(
    pagination: PaginationParams = Depends(),
    service: DeviceService = Depends(get_device_service),
):
    items, total = service.list(pagination.offset, pagination.page_size)
    return ApiResponse(
        data=PaginatedData(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )
    )
