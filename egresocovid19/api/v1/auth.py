from typing import Optional

from fastapi import Depends, Form, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel

from ...database import UserEntity
from ...services.auth_service import AuthService


class AccessTokenModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccessRefreshTokenModel(AccessTokenModel):
    refresh_token: str


class OAuth2RefreshTokenRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="refresh_token"),
        refresh_token: str = Form(...),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret


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
