from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import UserEntity
from ..auth import get_current_active_user

router = InferringRouter(tags=["Example"])


@cbv(router)
class BusinessController:
    current_user: UserEntity = Depends(get_current_active_user)

    @router.get("/example")
    async def example(self) -> str:
        return ""
