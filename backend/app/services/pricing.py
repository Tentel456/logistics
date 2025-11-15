from __future__ import annotations
from typing import Dict

from .routing import estimate_distance_km

# Simple pricing formula:
# price = base + distance_km * per_km + weight_kg * per_kg + volume_m3 * per_m3
# vehicle_factor (truck > van > bike/foot)
# sector coefficients could be added later

VEHICLE_FACTOR = {
    "truck": 1.3,
    "van": 1.1,
    "bike": 0.9,
    "foot": 0.8,
}

BASE = 2.0
PER_KM = 0.5
PER_KG = 0.02
PER_M3 = 0.5


def calculate_order_price(order_payload: Dict, vehicle_type: str | None = None) -> float:
    distance = estimate_distance_km(order_payload["from_lat"], order_payload["from_lon"], order_payload["to_lat"], order_payload["to_lon"])
    price = BASE + distance * PER_KM + order_payload["weight_kg"] * PER_KG + order_payload["volume_m3"] * PER_M3
    factor = VEHICLE_FACTOR.get(vehicle_type or "van", 1.0)
    return round(price * factor, 2)
