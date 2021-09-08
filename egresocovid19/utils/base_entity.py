from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from ..exceptions.not_found import NotFound


class BaseEntity(Document):
    async def update_from_model(self, model: BaseModel):
        await self.set(model.dict(exclude_unset=True))  # type: ignore

    @classmethod
    async def get_or_404(cls, id: PydanticObjectId):
        entity = await cls.get(id)
        if entity is None:
            raise NotFound(cls.__name__.removesuffix("Entity"))
        return entity
