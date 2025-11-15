from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt

from .config import settings

ROLES = {"admin","sector_manager","dispatcher","company","driver","warehouse"}


def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if role not in ROLES:
        raise ValueError("Unknown role")
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode = {"sub": subject, "role": role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
