from .database import MunicipalityEmbeddedEntity, ProvinceEntity
from .static.municipality_codes import municipality_codes
from .static.province_codes import province_codes


async def initialize_provinces_data():
    if not await ProvinceEntity.find_many().count():
        await ProvinceEntity.insert_many(
            [
                ProvinceEntity(
                    name=p_name,
                    code=p_code,
                    municipalities=list(
                        map(
                            lambda m: MunicipalityEmbeddedEntity(name=m[1], code=m[0]),
                            filter(
                                lambda m: m[0].startswith(p_code),
                                municipality_codes.items(),
                            ),
                        ),
                    ),
                )
                for p_code, p_name in province_codes.items()
            ]
        )
