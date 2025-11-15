from __future__ import annotations
from typing import Optional

from sqlmodel import Session, select

from ..db.models import Vehicle, Warehouse, Order


def fits_in_vehicle(order: Order, vehicle: Vehicle) -> bool:
    if order.weight_kg > (vehicle.max_weight_kg - (vehicle.current_load_kg or 0)):
        return False
    if order.volume_m3 > (vehicle.max_volume_m3 - (vehicle.current_load_m3 or 0)):
        return False
    if order.length_m > vehicle.length_m or order.width_m > vehicle.width_m or order.height_m > vehicle.height_m:
        return False
    return True


def find_vehicle_for_order(session: Session, order: Order) -> Optional[Vehicle]:
    vehicles = session.exec(select(Vehicle)).all()
    for v in vehicles:
        if fits_in_vehicle(order, v):
            return v
    return None


def find_warehouse_for_order(session: Session, order: Order) -> Optional[Warehouse]:
    warehouses = session.exec(select(Warehouse).where(Warehouse.active == True)).all()  # noqa: E712
    for w in warehouses:
        free = w.capacity_m3 - (w.used_m3 or 0)
        if order.volume_m3 <= free:
            return w
    return None
