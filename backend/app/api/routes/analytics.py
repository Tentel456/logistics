from fastapi import APIRouter, Depends

from ...api.deps import require_role
from ...services.analytics import overview

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview", dependencies=[Depends(require_role("admin","sector_manager"))])
async def analytics_overview():
    return overview()
