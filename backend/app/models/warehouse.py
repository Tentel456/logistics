from pydantic import BaseModel

class WarehouseIn(BaseModel):
    name: str
    capacity_m3: float
    lat: float
    lon: float

class WarehouseOut(WarehouseIn):
    id: str
    used_m3: float = 0
