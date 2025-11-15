from __future__ import annotations
from collections import defaultdict
from sqlmodel import Session, select

from ..db.models import Order, Vehicle, Warehouse


def overview(session: Session):
    orders = session.exec(select(Order)).all()
    by_status: dict[str, int] = defaultdict(int)
    for o in orders:
        by_status[o.status.value if hasattr(o.status, 'value') else str(o.status)] += 1
    return {
        "total_orders": len(orders),
        "orders_by_status": by_status,
        "vehicles": len(session.exec(select(Vehicle)).all()),
        "warehouses": len(session.exec(select(Warehouse)).all()),
    }
