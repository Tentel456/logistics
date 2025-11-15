from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...api.deps import require_role
from ...db.session import get_db
from ...db.models import Order as DBOrder, Assignment, Vehicle, Warehouse, OrderStatus
from ...models.order import OrderIn, OrderOut
from ...services.assignment import find_vehicle_for_order, find_warehouse_for_order
from ...services.pricing import calculate_order_price

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, dependencies=[Depends(require_role("admin","sector_manager","dispatcher","company"))])
async def create_order(payload: OrderIn, db: Session = Depends(get_db)):
    tracking = uuid4().hex[:10].upper()
    order = DBOrder(
        tracking_code=tracking,
        status=OrderStatus.created,
        **payload.model_dump(),
    )
    # preliminary pricing (vehicle type unknown yet, assume van)
    order.price = calculate_order_price(payload.model_dump(), vehicle_type="van")
    db.add(order)
    db.commit()
    db.refresh(order)

    # Auto-assign
    vehicle = find_vehicle_for_order(db, order)
    warehouse = find_warehouse_for_order(db, order)
    if vehicle or warehouse:
        assgn = Assignment(order_id=order.id, vehicle_id=getattr(vehicle, "id", None), warehouse_id=getattr(warehouse, "id", None))
        order.status = OrderStatus.assigned
        if vehicle:
            # refine price with vehicle type factor
            order.price = calculate_order_price(payload.model_dump(), vehicle_type=vehicle.type.value)
        db.add(assgn)
        db.add(order)
        db.commit()
        db.refresh(order)

    return OrderOut(
        id=str(order.id),
        tracking_code=order.tracking_code,
        status=order.status.value,
        price=order.price,
        **payload.model_dump(),
    )


@router.get("/track/{code}")
async def track_by_code(code: str, db: Session = Depends(get_db)):
    order = db.exec(select(DBOrder).where(DBOrder.tracking_code == code)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Tracking code not found")
    assgn = db.exec(select(Assignment).where(Assignment.order_id == order.id)).first()
    vehicle = db.get(Vehicle, assgn.vehicle_id) if assgn and assgn.vehicle_id else None
    warehouse = db.get(Warehouse, assgn.warehouse_id) if assgn and assgn.warehouse_id else None
    return {
        "order": order,
        "vehicle": vehicle,
        "warehouse": warehouse,
        "assignment": assgn,
    }


@router.post("/{order_id}/start", dependencies=[Depends(require_role("dispatcher","company","sector_manager"))])
async def start_transit(order_id: int, db: Session = Depends(get_db)):
    order = db.get(DBOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = OrderStatus.in_transit
    db.add(order)
    db.commit()
    return {"id": order.id, "status": order.status}


@router.post("/{order_id}/deliver", dependencies=[Depends(require_role("dispatcher","company","sector_manager","driver"))])
async def mark_delivered(order_id: int, db: Session = Depends(get_db)):
    order = db.get(DBOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = OrderStatus.delivered
    db.add(order)
    db.commit()
    return {"id": order.id, "status": order.status}
