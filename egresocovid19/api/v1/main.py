from fastapi import FastAPI
from fastapi_restful.api_settings import get_api_settings
from fastapi_restful.openapi import simplify_operation_ids

# For import all controllers dynamically
from . import controllers
from .controllers import *  # noqa: F401, F403


def create_api() -> FastAPI:
    get_api_settings.cache_clear()
    settings = get_api_settings()
    settings.title = "Egreso COVID-19 API"
    api = FastAPI(**settings.fastapi_kwargs)
    for item in dir(controllers):
        if item.endswith("_controller"):
            api.include_router(getattr(controllers, item).router)
    simplify_operation_ids(api)
    return api
