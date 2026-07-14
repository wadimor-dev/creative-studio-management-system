from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.product_movement import ProductMovementType
from app.schemas.product import ProductResponse
from app.schemas.location import LocationResponse
from app.schemas.user import UserResponse

class ProductMovementBase(BaseModel):
    product_id: int
    type: ProductMovementType
    quantity: int
    source_location_id: Optional[int] = None
    destination_location_id: Optional[int] = None
    reference: Optional[str] = None
    notes: Optional[str] = None

class ProductMovementCreate(ProductMovementBase):
    pass

class ProductMovementResponse(ProductMovementBase):
    id: int
    date: datetime
    user_id: int
    
    product: Optional[ProductResponse] = None
    source_location: Optional[LocationResponse] = None
    destination_location: Optional[LocationResponse] = None
    user: Optional[UserResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProductStockBase(BaseModel):
    product_id: int
    location_id: int
    quantity: int

class ProductStockResponse(ProductStockBase):
    id: int
    product: Optional[ProductResponse] = None
    location: Optional[LocationResponse] = None

    model_config = ConfigDict(from_attributes=True)

class StockOpnameItem(BaseModel):
    product_id: int
    actual_quantity: int

class StockOpnameRequest(BaseModel):
    location_id: int
    items: list[StockOpnameItem]
