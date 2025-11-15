from __future__ import annotations
from ..db.memory import DB
from ..models.enums import OrderStatus


def overview():
    total_orders = len(DB.orders)
    by_status = {s.value: 0 for s in OrderStatus}
    for o in DB.orders.values():
        by_status[o["status"]] = by_status.get(o["status"], 0) + 1
    return {
        "total_orders": total_orders,
        "orders_by_status": by_status,
        "vehicles": len(DB.vehicles),
        "warehouses": len(DB.warehouses),
    }
