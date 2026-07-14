from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel

T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
    success: bool
    message: str

class SuccessResponse(ResponseBase[T]):
    success: bool = True
    data: Optional[T] = None

class ErrorResponse(ResponseBase[Any]):
    success: bool = False
    errors: Optional[List[Any]] = None

def create_success_response(data: Any = None, message: str = "Success") -> dict:
    return {"success": True, "message": message, "data": data}

def create_error_response(message: str, errors: list = None) -> dict:
    return {"success": False, "message": message, "errors": errors or []}
