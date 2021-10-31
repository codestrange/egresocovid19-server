from beanie import Document, PydanticObjectId

from ..exceptions.not_found import NotFound


class BaseEntity(Document):
    @classmethod
    async def get_or_404(cls, id: PydanticObjectId):
        entity = await cls.get(id)
        if entity is None:
            suffix = "Entity"
            name = cls.__name__
            if cls.__name__.endswith(suffix):
                name = cls.__name__[: -len(suffix)]
            raise NotFound(name)
        return entity
