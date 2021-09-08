from pydantic import BaseModel


class DetailSchema(BaseModel):
    status_code: int
    detail: str
