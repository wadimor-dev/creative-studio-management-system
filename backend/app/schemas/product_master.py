from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base schema for all Product Master Data
class ProductMasterBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class ProductMasterCreate(ProductMasterBase):
    pass

class ProductMasterUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class ProductMasterResponse(ProductMasterBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
