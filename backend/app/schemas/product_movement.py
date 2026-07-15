from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.product_movement import ProductMovementType, ProductMovementReason
from app.schemas.product_placement import ProductPlacementResponse

class ProductMovementBase(BaseModel):
    product_id: int
    reason: ProductMovementReason
    quantity: int
    source_placement_id: Optional[int] = None
    destination_placement_id: Optional[int] = None
    reference: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    notes: Optional[str] = None

class ProductMovementCreate(ProductMovementBase):
    pass

class ProductMovementResponse(ProductMovementBase):
    id: int
    type: ProductMovementType
    date: datetime
    user_id: int
    
    source_placement: Optional[ProductPlacementResponse] = None
    destination_placement: Optional[ProductPlacementResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
