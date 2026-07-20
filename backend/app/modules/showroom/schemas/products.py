from pydantic import BaseModel
from typing import List, Optional


class ShowroomProductOption(BaseModel):
    id: int
    sku: str
    name: str


class ShowroomScanStock(BaseModel):
    product_id: int
    product_name: str
    sku: str
    quantity: int
    reserved_quantity: int = 0


class ShowroomScanPlacement(BaseModel):
    type: str = "placement"
    id: int
    code: Optional[str] = None
    slug: str
    name: str
    level: int = 1
    stocks: List[ShowroomScanStock] = []


class ShowroomScanProduct(BaseModel):
    type: str = "product"
    id: int
    sku: str
    display_name: str
    name: Optional[str] = None
