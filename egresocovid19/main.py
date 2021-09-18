from typing import List

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.main import create_api as create_api_v1
from .database import MunicipalityEmbeddedEntity, ProvinceEntity, client, entities
from .static.municipality_codes import municipality_codes
from .static.provinces_codes import province_codes

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1 = create_api_v1()
app.mount("/api/v1", api_v1)


@app.on_event("startup")
async def startup():
    await init_beanie(
        database=client.egresocovid19,
        document_models=entities,  # type: ignore
    )

    if not await ProvinceEntity.find_many().count():
        provinces: List[ProvinceEntity] = []
        for province_code, province_name in province_codes.items():
            municipalities: List[MunicipalityEmbeddedEntity] = []
            for municipality_code, municipality_name in municipality_codes.items():
                if municipality_code[:2] == province_code:
                    municipalities.append(
                        MunicipalityEmbeddedEntity(
                            name=municipality_name,
                        )
                    )
            provinces.append(
                ProvinceEntity(
                    name=province_name,
                    municipalities=municipalities,
                )
            )
        await ProvinceEntity.insert_many(provinces)


@app.on_event("shutdown")
async def shutdown():
    pass
