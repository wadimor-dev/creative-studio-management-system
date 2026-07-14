from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
