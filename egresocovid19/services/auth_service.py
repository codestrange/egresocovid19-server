from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..database import UserEntity
from ..settings import Settings, get_settings


class AuthService:
    def __init__(
        self,
        settings: Settings = Depends(get_settings),
    ):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> Optional[UserEntity]:
        user = await UserEntity.find_one(UserEntity.email == email)
        if user and self.verify_password(password, user.hashed_password):
            return user

    def create_access_token(
        self,
        user_or_id: Union[UserEntity, str],
        expires_delta: timedelta = timedelta(minutes=15),
    ) -> str:
        return self._create_generic_token(
            user_or_id,
            expires_delta,
            self.settings.access_token_secret_key,
            self.settings.access_token_algorithm,
        )

    def create_refresh_token(
        self,
        user_or_id: Union[UserEntity, str],
        expires_delta: timedelta = timedelta(minutes=24 * 60),
    ) -> str:
        return self._create_generic_token(
            user_or_id,
            expires_delta,
            self.settings.refresh_token_secret_key,
            self.settings.refresh_token_algorithm,
        )

    def _create_generic_token(
        self,
        user_or_id: Union[UserEntity, str],
        expires_delta: timedelta,
        secret_key: str,
        algorithm: str,
    ) -> str:
        to_encode: dict = {}
        if isinstance(user_or_id, UserEntity):
            to_encode["sub"] = str(user_or_id.id)
        else:
            to_encode["sub"] = str(user_or_id)
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    async def get_user_by_access_token(
        self,
        access_token: str,
    ) -> Optional[UserEntity]:
        return await self._get_user_by_generic_token(
            access_token,
            self.settings.access_token_secret_key,
            self.settings.access_token_algorithm,
        )

    async def get_user_by_refresh_token(
        self,
        refresh_token: str,
    ) -> Optional[UserEntity]:
        return await self._get_user_by_generic_token(
            refresh_token,
            self.settings.refresh_token_secret_key,
            self.settings.refresh_token_algorithm,
        )

    async def _get_user_by_generic_token(
        self,
        token: str,
        secret_key: str,
        algorithm: str,
    ) -> Optional[UserEntity]:
        try:
            decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
            user = await UserEntity.get(decoded_jwt["sub"])
            return user
        except JWTError:
            return None
