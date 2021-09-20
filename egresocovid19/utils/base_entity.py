from beanie import Document, PydanticObjectId

from ..exceptions.not_found import NotFound


class BaseEntity(Document):
    @classmethod
    async def get_or_404(cls, id: PydanticObjectId):
        entity = await cls.get(id)
        if entity is None:
            raise NotFound(cls.__name__.removesuffix("Entity"))
        return entity
