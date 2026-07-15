from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from app.models.product_movement import ProductMovementType, ProductMovementReason

if TYPE_CHECKING:
    from app.schemas.product import ProductResponse

# --- Placement Type ---
class PlacementTypeBase(BaseModel):
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None

class PlacementTypeCreate(PlacementTypeBase):
    pass

class PlacementTypeUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class PlacementTypeResponse(PlacementTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Product Placement ---
class ProductPlacementBase(BaseModel):
    name: str
    code: Optional[str] = None
    type_id: int
    parent_id: Optional[int] = None
    level: int = 1
    is_active: bool = True

class ProductPlacementCreate(ProductPlacementBase):
    pass

class ProductPlacementUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type_id: Optional[int] = None
    parent_id: Optional[int] = None
    level: Optional[int] = None
    is_active: Optional[bool] = None

class ProductPlacementResponse(ProductPlacementBase):
    id: int
    placement_type: Optional[PlacementTypeResponse] = None
    model_config = ConfigDict(from_attributes=True)

class ProductPlacementHierarchyResponse(ProductPlacementResponse):
    children: List['ProductPlacementHierarchyResponse'] = []
    model_config = ConfigDict(from_attributes=True)

# --- Product Placement Stock ---
from app.schemas.product import ProductResponse

class ProductPlacementStockResponse(BaseModel):
    id: int
    product_id: int
    placement_id: int
    quantity: int
    reserved_quantity: int
    
    placement: Optional[ProductPlacementResponse] = None
    product: Optional[ProductResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
