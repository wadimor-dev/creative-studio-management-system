from typing import Optional
from pydantic import BaseModel


class PositionBase(BaseModel):
    department_id: int
    name: str
    code: str
    description: Optional[str] = None
    is_active: bool = True


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    department_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PositionResponse(PositionBase):
    id: int

    class Config:
        from_attributes = True
