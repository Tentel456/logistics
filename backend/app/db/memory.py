from __future__ import annotations
from typing import Dict, List
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class InMemoryDB:
    users: Dict[str, dict] = field(default_factory=dict)
    vehicles: Dict[str, dict] = field(default_factory=dict)
    warehouses: Dict[str, dict] = field(default_factory=dict)
    orders: Dict[str, dict] = field(default_factory=dict)
    assignments: Dict[str, dict] = field(default_factory=dict)  # order_id -> {vehicle_id, warehouse_id}

    def gen_id(self) -> str:
        return uuid4().hex

DB = InMemoryDB()
