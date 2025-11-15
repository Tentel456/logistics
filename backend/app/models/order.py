from pydantic import BaseModel
from .enums import OrderStatus

class OrderIn(BaseModel):
    weight_kg: float
    volume_m3: float
    length_m: float
    width_m: float
    height_m: float
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float
    item_type: str

class OrderOut(OrderIn):
    id: str
    tracking_code: str
    status: OrderStatus
    price: float
