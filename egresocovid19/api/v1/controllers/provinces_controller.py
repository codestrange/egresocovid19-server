from typing import List

from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from pydantic import parse_obj_as

from ....database import UserEntity
from ....services.province_service import ProvinceService
from ..auth import get_current_active_user
from ..schemas import ProvinceSchema

router = InferringRouter(tags=["Provinces"])


@cbv(router)
class ProvincesController:
    current_user: UserEntity = Depends(get_current_active_user)
    province_service: ProvinceService = Depends()

    @router.get("/provinces")
    def get_provinces(self) -> List[ProvinceSchema]:
        provinces = self.province_service.get_provinces()
        return parse_obj_as(List[ProvinceSchema], provinces)
