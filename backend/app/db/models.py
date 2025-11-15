from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class VehicleType(str, Enum):
    van = "van"
    truck = "truck"
    bike = "bike"
    foot = "foot"

class OrderStatus(str, Enum):
    created = "created"
    assigned = "assigned"
    in_transit = "in_transit"
    delivered = "delivered"
    failed = "failed"

class Vehicle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: VehicleType
    max_weight_kg: float
    max_volume_m3: float
    length_m: float
    width_m: float
    height_m: float
    current_load_kg: float = 0
    current_load_m3: float = 0
    lat: Optional[float] = None
    lon: Optional[float] = None

class Warehouse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    capacity_m3: float
    used_m3: float = 0
    lat: float
    lon: float
    active: bool = True

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tracking_code: str
    status: OrderStatus
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
    price: float = 0

class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    vehicle_id: Optional[int] = Field(default=None, foreign_key="vehicle.id")
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouse.id")
