from typing import List

from beanie import init_beanie
from beanie.odm.queries.find import FindMany
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

    if await FindMany(ProvinceEntity).count() == 0:
        for province_code in province_codes:
            municipalities: List[MunicipalityEmbeddedEntity] = []
            for municip_code in municipality_codes:
                if municip_code[:2] == province_code:
                    municipalities.append(
                        MunicipalityEmbeddedEntity(
                            name=municipality_codes[municip_code]
                        )
                    )
            await ProvinceEntity.insert_one(
                ProvinceEntity(
                    name=province_codes[province_code], municipalities=municipalities
                )
            )


@app.on_event("shutdown")
async def shutdown():
    pass
