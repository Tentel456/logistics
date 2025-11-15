from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ...api.deps import require_role
from ...db.memory import DB
from ...models.enums import OrderStatus
from ...services.assignment import find_vehicle_for_order

router = APIRouter(prefix="/events", tags=["events"])

class EmergencyStop(BaseModel):
    order_id: str

@router.post("/emergency_stop", dependencies=[Depends(require_role("dispatcher","driver"))])
async def emergency_stop(evt: EmergencyStop):
    order = DB.orders.get(evt.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # free current assignment and find another vehicle
    assgn = DB.assignments.get(evt.order_id)
    if assgn:
        assgn["vehicle_id"] = None
    new_vid = find_vehicle_for_order(order)
    if new_vid:
        DB.assignments[evt.order_id] = {"vehicle_id": new_vid, "warehouse_id": (assgn or {}).get("warehouse_id")}
        order["status"] = OrderStatus.assigned.value
        return {"reassigned_to_vehicle": new_vid}
    order["status"] = OrderStatus.failed.value
    return {"message": "No alternate vehicle available", "status": order["status"]}
