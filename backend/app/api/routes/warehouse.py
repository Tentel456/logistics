from fastapi import APIRouter, Depends

from ...api.deps import require_role
from ...db.memory import DB
from ...models.warehouse import WarehouseIn, WarehouseOut

router = APIRouter(prefix="/warehouses", tags=["warehouse"])

@router.post("", response_model=WarehouseOut, dependencies=[Depends(require_role("admin","warehouse","sector_manager"))])
async def register_warehouse(payload: WarehouseIn):
    wid = DB.gen_id()
    data = payload.model_dump()
    data.update({"id": wid, "used_m3": 0.0})
    DB.warehouses[wid] = data
    return data

@router.get("")
async def list_warehouses():
    return list(DB.warehouses.values())
