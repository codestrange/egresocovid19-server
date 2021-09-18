from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.main import create_api as create_api_v1
from .database import client, entities
from .seedbed import initialize_provinces_data

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
    await initialize_provinces_data()


@app.on_event("shutdown")
async def shutdown():
    pass
