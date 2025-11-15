from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...api.deps import require_role
from ...db.session import get_db
from ...db.models import Warehouse
from ...models.warehouse import WarehouseIn, WarehouseOut

router = APIRouter(prefix="/warehouses", tags=["warehouse"])


@router.post("", response_model=WarehouseOut, dependencies=[Depends(require_role("admin","warehouse","sector_manager"))])
async def register_warehouse(payload: WarehouseIn, db: Session = Depends(get_db)):
    w = Warehouse(**payload.model_dump(), used_m3=0.0, active=True)
    db.add(w)
    db.commit()
    db.refresh(w)
    return WarehouseOut(id=str(w.id), name=w.name, capacity_m3=w.capacity_m3, used_m3=w.used_m3, lat=w.lat, lon=w.lon)


@router.get("")
async def list_warehouses(db: Session = Depends(get_db)):
    return db.exec(select(Warehouse)).all()


@router.post("/{warehouse_id}/deactivate", dependencies=[Depends(require_role("admin","sector_manager"))])
async def deactivate_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    w = db.get(Warehouse, warehouse_id)
    if not w:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    w.active = False
    db.add(w)
    db.commit()
    return {"id": w.id, "active": w.active}


@router.post("/{warehouse_id}/activate", dependencies=[Depends(require_role("admin","sector_manager"))])
async def activate_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    w = db.get(Warehouse, warehouse_id)
    if not w:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    w.active = True
    db.add(w)
    db.commit()
    return {"id": w.id, "active": w.active}
