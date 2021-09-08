from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr

from .settings import get_settings
from .utils.base_entity import BaseEntity

client = AsyncIOMotorClient(get_settings().database_url)


class UserEntity(BaseEntity):
    name: str
    email: EmailStr
    phone: str
    hashed_password: str
    email_confirmed: bool = False
    phone_confirmed: bool = False
    disabled: bool = False

    class Collection:
        name: str = "users"


entities = [
    UserEntity,
]
