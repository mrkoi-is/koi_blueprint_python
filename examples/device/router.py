from fastapi import APIRouter, Depends, status

from app.core.responses import ApiResponse

from .schemas import DeviceCreateSchema, DeviceResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[DeviceResponse])
def create_device(payload: DeviceCreateSchema):
    _ = payload
    raise NotImplementedError("Wire this example to a concrete service in your project")
