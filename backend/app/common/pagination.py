from typing import Generic, TypeVar, List
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")

class MetaData(BaseModel):
    total: int
    page: int
    size: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: List[T]
    meta: MetaData

def create_paginated_response(data: list, total: int, page: int, size: int, message: str = "Success") -> dict:
    total_pages = (total + size - 1) // size if size > 0 else 0
    meta = {
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta
    }

class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(10, ge=1, le=100, description="Items per page")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size
