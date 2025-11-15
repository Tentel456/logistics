from fastapi import APIRouter, Depends

from ...api.deps import require_role
from ...db.memory import DB
from ...models.vehicle import VehicleIn, VehicleOut

router = APIRouter(prefix="/vehicles", tags=["transport"])

@router.post("", response_model=VehicleOut, dependencies=[Depends(require_role("admin","company"))])
async def register_vehicle(payload: VehicleIn):
    vid = DB.gen_id()
    data = payload.model_dump()
    data.update({"id": vid, "current_load_kg": 0.0, "current_load_m3": 0.0})
    DB.vehicles[vid] = data
    return data

@router.get("")
async def list_vehicles():
    return list(DB.vehicles.values())
