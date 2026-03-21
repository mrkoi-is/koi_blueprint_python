from pydantic import BaseModel


class DeviceCreateSchema(BaseModel):
    sn: str
    name: str


class DeviceResponse(BaseModel):
    id: int
    sn: str
    name: str
    status: str

    model_config = {"from_attributes": True}
