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

    # Simple truck-aware constraints
    v_len = payload.get("vehicle_length_m")
    v_wid = payload.get("vehicle_width_m")
    v_hei = payload.get("vehicle_height_m")

    constraints_ok = True
    constraints = []
    # Clearance limits (example heuristics)
    BRIDGE_CLEARANCE_M = 4.0
    NARROW_STREET_WIDTH_M = 2.2

    if v_hei is not None and v_hei > BRIDGE_CLEARANCE_M:
        constraints_ok = False
        constraints.append(f"height {v_hei}m exceeds assumed clearance {BRIDGE_CLEARANCE_M}m")
    if v_wid is not None and v_wid > NARROW_STREET_WIDTH_M:
        # not blocking but add note
        constraints.append("wide vehicle may require detours; avoid narrow streets")

    return {
        "distance_km": round(distance_km, 2),
        "eta_hours": round(eta_h, 2) if eta_h is not None else None,
        "constraints_ok": constraints_ok,
        "constraints": constraints,
        "notes": "Demo truck-aware routing check. Replace with map provider integration for real constraints.",
    }
