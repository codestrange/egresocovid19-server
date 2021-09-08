from typing import Optional

from fastapi import HTTPException, status


class NotFound(HTTPException):
    def __init__(self, object_name: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{object_name if object_name else 'Entity'} not found",
        )
