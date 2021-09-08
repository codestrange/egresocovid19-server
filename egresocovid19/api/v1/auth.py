from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel

from ...database import UserEntity
from ...services.auth_service import AuthService


class TokenModel(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    expires_in: int


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(),
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await auth_service.get_user_by_access_token(token)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    user: UserEntity = Depends(get_current_user),
) -> UserEntity:
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return user
