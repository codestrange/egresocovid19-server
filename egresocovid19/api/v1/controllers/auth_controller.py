from datetime import timedelta
from typing import Optional

from fastapi import Depends, Form, HTTPException, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import UserEntity
from ....services.auth_service import AuthService
from ....settings import Settings, get_settings
from ....utils.bad_request_response import bad_request_response
from ....utils.forbidden_response import forbidden_response
from ..auth import TokenModel

router = InferringRouter(tags=["Authentication"])


@cbv(router)
class AuthController:
    auth_service: AuthService = Depends()
    settings: Settings = Depends(get_settings)

    @router.post(
        "/auth/token",
        responses={
            400: bad_request_response,
            401: forbidden_response,
        },
    )
    async def authentication(
        self,
        grant_type: str = Form(
            ...,
            description="password or refresh_token",
        ),
        username: Optional[str] = Form(
            None,
            description="required for password grant type",
        ),
        password: Optional[str] = Form(
            None,
            description="required for password grant type",
        ),
        scope: str = Form(
            "",
            description="only use when grant type is password",
        ),
        refresh_token: Optional[str] = Form(
            None,
            description="required for refresh_token grant type",
        ),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ) -> TokenModel:
        user: Optional[UserEntity] = None
        if grant_type == "password":
            if username and password:
                user = await self.auth_service.authenticate_user(
                    email=username,
                    password=password,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="username or password are required in password grant type",
                )
        elif grant_type == "refresh_token":
            if refresh_token:
                user = await self.auth_service.get_user_by_refresh_token(
                    refresh_token=refresh_token,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="refresh_token is required in refresh_token grant type",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid grant type",
            )
        if not user:
            if grant_type == "password":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            elif grant_type == "refresh_token":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect refresh token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        access_token = self.auth_service.create_access_token(
            user=user,
            expires_delta=timedelta(
                minutes=self.settings.access_token_expire_minutes,
            ),
        )
        refresh_token = self.auth_service.create_refresh_token(
            user=user,
            expires_delta=timedelta(
                minutes=self.settings.refresh_token_expire_minutes,
            ),
        )
        return TokenModel(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.settings.access_token_expire_minutes * 60,
        )
