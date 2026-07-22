from typing import Optional
from pydantic import BaseModel, ConfigDict


class BankCreate(BaseModel):
    code: str
    name: str
    short_name: Optional[str] = None
    is_active: bool = True


class BankUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    short_name: Optional[str] = None
    is_active: Optional[bool] = None


class BankResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    short_name: Optional[str] = None
    is_active: bool
