from typing import List

from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import ProvinceEntity, UserEntity
from ..auth import get_current_active_user

router = InferringRouter(tags=["Provinces"])


@cbv(router)
class ProvincesController:
    current_user: UserEntity = Depends(get_current_active_user)

    @router.get("/provinces")
    async def get_provinces(self) -> List[ProvinceEntity]:
        return await ProvinceEntity.find_all().to_list()
