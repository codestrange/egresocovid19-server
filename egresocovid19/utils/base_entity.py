from typing import Type, TypeVar

from beanie import Document, PydanticObjectId

from ..exceptions.not_found import NotFound

T = TypeVar("T", bound=Document)


class BaseEntity(Document):
    @classmethod
    async def get_or_404(cls: Type[T], id: PydanticObjectId) -> T:
        entity = await cls.get(id)
        if entity is None:
            suffix = "Entity"
            name = cls.__name__
            if cls.__name__.endswith(suffix):
                name = cls.__name__[: -len(suffix)]
            raise NotFound(name)
        return entity
