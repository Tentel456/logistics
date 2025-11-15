from __future__ import annotations
from typing import Optional

from ..db.memory import DB


def fits_in_vehicle(order: dict, vehicle: dict) -> bool:
    if order["weight_kg"] > (vehicle["max_weight_kg"] - vehicle.get("current_load_kg", 0)):
        return False
    if order["volume_m3"] > (vehicle["max_volume_m3"] - vehicle.get("current_load_m3", 0)):
        return False
    # dimension check (simplified)
    if order["length_m"] > vehicle["length_m"] or order["width_m"] > vehicle["width_m"] or order["height_m"] > vehicle["height_m"]:
        return False
    return True


def find_vehicle_for_order(order: dict) -> Optional[str]:
    # naive: pick first that fits
    for vid, v in DB.vehicles.items():
        if fits_in_vehicle(order, v):
            return vid
    return None


def find_warehouse_for_order(order: dict) -> Optional[str]:
    # naive: any with free capacity
    for wid, w in DB.warehouses.items():
        free = w["capacity_m3"] - w.get("used_m3", 0)
        if order["volume_m3"] <= free:
            return wid
    return None
