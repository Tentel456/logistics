from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ...api.deps import require_role
from ...db.session import get_db
from ...db.models import Order as DBOrder, Assignment, Vehicle, Warehouse, OrderStatus
from ...services.assignment import find_vehicle_for_order, find_warehouse_for_order

router = APIRouter(prefix="/events", tags=["events"])


class EmergencyStop(BaseModel):
    order_id: int


@router.post("/emergency_stop", dependencies=[Depends(require_role("dispatcher","driver"))])
async def emergency_stop(evt: EmergencyStop, db: Session = Depends(get_db)):
    order = db.get(DBOrder, evt.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    assgn = db.exec(select(Assignment).where(Assignment.order_id == order.id)).first()
    if assgn:
        assgn.vehicle_id = None
        db.add(assgn)
    new_vehicle = find_vehicle_for_order(db, order)
    if new_vehicle:
        if not assgn:
            assgn = Assignment(order_id=order.id)
        assgn.vehicle_id = new_vehicle.id
        order.status = OrderStatus.assigned
        db.add(assgn)
        db.add(order)
        db.commit()
        return {"reassigned_to_vehicle": new_vehicle.id}
    order.status = OrderStatus.failed
    db.add(order)
    db.commit()
    return {"message": "No alternate vehicle available", "status": order.status}


class Breakdown(BaseModel):
    vehicle_id: int
    order_id: int


@router.post("/breakdown", dependencies=[Depends(require_role("dispatcher","driver"))])
async def vehicle_breakdown(evt: Breakdown, db: Session = Depends(get_db)):
    order = db.get(DBOrder, evt.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    assgn = db.exec(select(Assignment).where(Assignment.order_id == order.id)).first()
    if assgn:
        assgn.vehicle_id = None
        db.add(assgn)
    new_vehicle = find_vehicle_for_order(db, order)
    if new_vehicle:
        if not assgn:
            assgn = Assignment(order_id=order.id)
        assgn.vehicle_id = new_vehicle.id
        order.status = OrderStatus.assigned
        db.add(assgn)
        db.add(order)
        db.commit()
        return {"reassigned_to_vehicle": new_vehicle.id}
    order.status = OrderStatus.failed
    db.add(order)
    db.commit()
    return {"message": "No alternate vehicle available", "status": order.status}


class WarehouseIncident(BaseModel):
    warehouse_id: int
    mode: str  # "fire" | "overflow"
    order_id: int | None = None


@router.post("/warehouse_incident", dependencies=[Depends(require_role("dispatcher","sector_manager","admin"))])
async def warehouse_incident(evt: WarehouseIncident, db: Session = Depends(get_db)):
    w = db.get(Warehouse, evt.warehouse_id)
    if not w:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    # deactivate warehouse for fire/overflow
    w.active = False
    db.add(w)
    db.commit()

    # Try to reassign order if provided
    if evt.order_id is not None:
        order = db.get(DBOrder, evt.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        assgn = db.exec(select(Assignment).where(Assignment.order_id == order.id)).first()
        if assgn:
            assgn.warehouse_id = None
            db.add(assgn)
        new_wh = find_warehouse_for_order(db, order)
        if new_wh:
            if not assgn:
                assgn = Assignment(order_id=order.id)
            assgn.warehouse_id = new_wh.id
            db.add(assgn)
            db.commit()
            return {"reassigned_to_warehouse": new_wh.id, "warehouse_active": w.active}
        return {"message": "No alternate warehouse available", "warehouse_active": w.active}

    return {"warehouse_id": w.id, "active": w.active}
