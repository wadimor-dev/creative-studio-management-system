from typing import Optional
from pydantic import BaseModel


class DivisionBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class DivisionCreate(DivisionBase):
    pass


class DivisionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DivisionResponse(DivisionBase):
    id: int

    class Config:
        from_attributes = True
