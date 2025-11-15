from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException

from ...api.deps import require_role
from ...db.memory import DB
from ...models.order import OrderIn, OrderOut
from ...models.enums import OrderStatus
from ...services.assignment import find_vehicle_for_order, find_warehouse_for_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, dependencies=[Depends(require_role("admin","sector_manager","dispatcher","company"))])
async def create_order(payload: OrderIn):
    oid = DB.gen_id()
    tracking = uuid4().hex[:10].upper()
    order = payload.model_dump()
    order.update({"id": oid, "tracking_code": tracking, "status": OrderStatus.created.value})
    DB.orders[oid] = order

    # Auto-assign naive
    vid = find_vehicle_for_order(order)
    wid = find_warehouse_for_order(order)
    if vid or wid:
        DB.assignments[oid] = {"vehicle_id": vid, "warehouse_id": wid}
        order["status"] = OrderStatus.assigned.value

    return order

@router.get("/track/{code}")
async def track_by_code(code: str):
    for o in DB.orders.values():
        if o["tracking_code"] == code:
            assgn = DB.assignments.get(o["id"]) or {}
            vehicle = DB.vehicles.get(assgn.get("vehicle_id")) if assgn.get("vehicle_id") else None
            return {
                "order": o,
                "vehicle": vehicle,
                "assignment": assgn,
            }
    raise HTTPException(status_code=404, detail="Tracking code not found")
