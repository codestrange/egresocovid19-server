from typing import Optional

from fastapi import HTTPException, status


class Forbidden(HTTPException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message if message else "Forbidden",
        )
