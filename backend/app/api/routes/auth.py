from fastapi import APIRouter
from pydantic import BaseModel

from ...core.security import create_access_token, ROLES

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenRequest(BaseModel):
    email: str
    role: str

@router.post("/token")
async def issue_token(body: TokenRequest):
    role = body.role
    if role not in ROLES:
        return {"error": "Unknown role", "allowed": sorted(list(ROLES))}
    token = create_access_token(subject=body.email, role=role)
    return {"access_token": token, "token_type": "bearer"}
