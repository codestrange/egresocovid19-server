from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....services.auth_service import AuthService
from ....settings import Settings, get_settings
from ..auth import (
    AccessRefreshTokenModel,
    AccessTokenModel,
    OAuth2RefreshTokenRequestForm,
)

router = InferringRouter(tags=["Authentication"])


@cbv(router)
class AuthController:
    auth_service: AuthService = Depends()
    settings: Settings = Depends(get_settings)

    @router.post("/auth/token")
    async def access_token(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ) -> AccessRefreshTokenModel:
        user = await self.auth_service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.auth_service.create_access_token(
            user_or_id=user,
            expires_delta=timedelta(
                minutes=self.settings.access_token_expire_minutes,
            ),
        )
        refresh_token = self.auth_service.create_refresh_token(
            user_or_id=user,
            expires_delta=timedelta(
                minutes=self.settings.refresh_token_expire_minutes,
            ),
        )
        return AccessRefreshTokenModel(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @router.post("/auth/refresh")
    async def refresh_token(
        self,
        form_data: OAuth2RefreshTokenRequestForm = Depends(),
    ) -> AccessTokenModel:
        user = await self.auth_service.get_user_by_refresh_token(
            refresh_token=form_data.refresh_token,
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.auth_service.create_access_token(
            user_or_id=user,
            expires_delta=timedelta(
                minutes=self.settings.access_token_expire_minutes,
            ),
        )
        return AccessTokenModel(access_token=access_token)
