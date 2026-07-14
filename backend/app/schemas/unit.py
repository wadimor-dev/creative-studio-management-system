from pydantic import BaseModel, ConfigDict
from typing import Optional

class UnitBase(BaseModel):
    name: str
    description: Optional[str] = None

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    name: Optional[str] = None

class UnitResponse(UnitBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
