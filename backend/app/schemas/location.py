from pydantic import BaseModel, ConfigDict
from typing import Optional

class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    name: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
