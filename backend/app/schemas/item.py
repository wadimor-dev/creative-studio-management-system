from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.category import CategoryResponse
from app.schemas.unit import UnitResponse
from app.schemas.location import LocationResponse

class ItemBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    location_id: Optional[int] = None

class ItemCreate(ItemBase):
    initial_stock: Optional[int] = 0

class ItemUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    location_id: Optional[int] = None
    stock_qty: Optional[int] = None

class ItemResponse(ItemBase):
    id: int
    stock_qty: int
    
    category: Optional[CategoryResponse] = None
    unit: Optional[UnitResponse] = None
    location: Optional[LocationResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
