from fastapi import HTTPException, Query, Path
from typing import Optional
import uuid
from app.utils.validator import is_positive

def validate_uuid(id: str = Path(..., description="The UUID of the resource")):
    try:
        val = uuid.UUID(id, version=4)
        return str(val)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

def validate_positive(
    amount: int = Query(..., description="Amount must be positive")
):
    if not is_positive(amount):
        raise HTTPException(status_code=400, detail="Value must be positive")
    return amount

class PaginationDependency:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(10, ge=1, le=100, description="Items per page")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size

def validate_pagination(params: PaginationDependency = None):
    # This dependency can be used as Depends(validate_pagination)
    return params
