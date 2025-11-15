from fastapi import APIRouter, Depends
from sqlmodel import Session

from ...api.deps import require_role
from ...db.session import get_db
from ...services.analytics import overview

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", dependencies=[Depends(require_role("admin","sector_manager"))])
async def analytics_overview(db: Session = Depends(get_db)):
    return overview(db)
