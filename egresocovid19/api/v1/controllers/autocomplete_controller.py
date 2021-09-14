from typing import List

from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import UserEntity
from ....services.autocomplete_service import AutoCompleteService
from ..auth import get_current_active_user

router = InferringRouter(tags=["Auto Complete"])


@cbv(router)
class AutoCompleteController:
    current_user: UserEntity = Depends(get_current_active_user)
    autocomplete_service: AutoCompleteService = Depends()

    @router.get("/autocomplete/polyclinics/{query}")
    async def get_polyclinics(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_polyclinics(query)]

    @router.get("/autocomplete/surgeries/{query}")
    async def get_surgeries(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_surgeries(query)]

    @router.get("/autocomplete/popular_councils/{query}")
    async def get_popular_councils(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_popular_councils(query)]

    @router.get("/autocomplete/neighborhoods/{query}")
    async def get_neighborhoods(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_neighborhoods(query)]

    @router.get("/autocomplete/pathologicals/{query}")
    async def get_pathologicals(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_pathologicals(query)]

    @router.get("/autocomplete/default_pathologicals")
    async def get_default_pathologicals(self) -> List[str]:
        return [i async for i in self.autocomplete_service.get_default_pathologicals()]

    @router.get("/autocomplete/antibiotics/{query}")
    async def get_antibiotics(self, query: str) -> List[str]:
        return [i for i in await self.autocomplete_service.get_antibiotics(query)]

    @router.get("/autocomplete/another_vaccines_against_covid/{query}")
    async def get_another_vaccines_against_covid(self, query: str) -> List[str]:
        gen = self.autocomplete_service.get_another_vaccines_against_covid(query)
        return [i async for i in gen]

    @router.get("/autocomplete/others_aftermaths/{query}")
    async def get_others_aftermaths(self, query: str) -> List[str]:
        return [i for i in await self.autocomplete_service.get_others_aftermaths(query)]

    @router.get("/autocomplete/symptoms/{query}")
    async def get_symptoms(self, query: str) -> List[str]:
        return [i async for i in self.autocomplete_service.get_symptoms(query)]

    @router.get("/autocomplete/default_symptoms")
    async def get_default_symptoms(self) -> List[str]:
        return [i async for i in self.autocomplete_service.get_default_symptoms()]
