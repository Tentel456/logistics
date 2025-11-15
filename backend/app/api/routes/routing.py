from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...api.deps import require_role
from ...services.routing import plan_route

router = APIRouter(prefix="/routing", tags=["routing"])

class RouteRequest(BaseModel):
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float
    vehicle_length_m: float | None = None
    vehicle_width_m: float | None = None
    vehicle_height_m: float | None = None

@router.post("/route", dependencies=[Depends(require_role("admin","dispatcher","sector_manager"))])
async def route(req: RouteRequest):
    return plan_route(req.model_dump())
