from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ...api.deps import require_role
from ...db.session import get_db
from ...db.models import Vehicle
from ...models.vehicle import VehicleIn, VehicleOut

router = APIRouter(prefix="/vehicles", tags=["transport"])


@router.post("", response_model=VehicleOut, dependencies=[Depends(require_role("admin","company"))])
async def register_vehicle(payload: VehicleIn, db: Session = Depends(get_db)):
    v = Vehicle(**payload.model_dump(), current_load_kg=0.0, current_load_m3=0.0)
    db.add(v)
    db.commit()
    db.refresh(v)
    return VehicleOut(**payload.model_dump(), id=str(v.id), current_load_kg=v.current_load_kg, current_load_m3=v.current_load_m3)


@router.get("")
async def list_vehicles(db: Session = Depends(get_db)):
    vehicles = db.exec(select(Vehicle)).all()
    return vehicles
