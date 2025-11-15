from pydantic import BaseModel, Field
from .enums import VehicleType

class VehicleIn(BaseModel):
    name: str
    type: VehicleType
    max_weight_kg: float
    max_volume_m3: float
    length_m: float
    width_m: float
    height_m: float

class VehicleOut(VehicleIn):
    id: str
    company_id: str | None = Field(default=None)
    current_load_kg: float = 0
    current_load_m3: float = 0
    lat: float | None = None
    lon: float | None = None
