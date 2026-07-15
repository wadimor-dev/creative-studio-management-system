from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
