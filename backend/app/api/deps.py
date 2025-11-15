from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from ..core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user_role(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        role: str = payload.get("role")
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no role")
        return role
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def require_role(*allowed: str):
    def dep(role: Annotated[str, Depends(get_current_user_role)]):
        if role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return role
    return dep
