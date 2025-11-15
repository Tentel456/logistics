from __future__ import annotations
from math import hypot
from typing import Dict, Any


def estimate_distance_km(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    # dummy Euclidean approx; replace with real routing
    return hypot(a_lat - b_lat, a_lon - b_lon) * 111.0


def plan_route(payload: Dict[str, Any]) -> Dict[str, Any]:
    distance_km = estimate_distance_km(payload["from_lat"], payload["from_lon"], payload["to_lat"], payload["to_lon"])
    speed_kmh = 40.0  # naive city avg
    eta_h = distance_km / speed_kmh if speed_kmh else None
    return {
        "distance_km": round(distance_km, 2),
        "eta_hours": round(eta_h, 2) if eta_h is not None else None,
        "constraints_ok": True,
        "notes": "Demo route planner. For production, integrate with truck-aware routing APIs.",
    }
