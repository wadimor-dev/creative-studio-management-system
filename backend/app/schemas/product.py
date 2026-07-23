from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models.product import ProductStatus
from app.schemas.product_master import ProductMasterResponse

class ProductBase(BaseModel):
    type_id: int
    category_id: int
    motif_id: int
    sub_motif_id: Optional[int] = None
    color_id: Optional[int] = None
    
    variant: Optional[str] = None
    image_url: Optional[str] = None
    status: ProductStatus = ProductStatus.ACTIVE

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    type_id: Optional[int] = None
    category_id: Optional[int] = None
    motif_id: Optional[int] = None
    sub_motif_id: Optional[int] = None
    color_id: Optional[int] = None
    variant: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[ProductStatus] = None

class ProductResponse(ProductBase):
    id: int
    sku: str
    display_name: str
    
    # Nested master data
    type: Optional[ProductMasterResponse] = None
    category: Optional[ProductMasterResponse] = None
    motif: Optional[ProductMasterResponse] = None
    sub_motif: Optional[ProductMasterResponse] = None
    color: Optional[ProductMasterResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
