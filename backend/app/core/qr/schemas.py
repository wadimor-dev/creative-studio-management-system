from typing import Optional
from pydantic import BaseModel


class QREntityCreate(BaseModel):
    entity_type: str
    entity_id: int
    label: Optional[str] = None
    storage_location_id: Optional[int] = None


class QREntityUpdate(BaseModel):
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    label: Optional[str] = None
    storage_location_id: Optional[int] = None
    is_active: Optional[bool] = None


class QREntityResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    token: str
    label: Optional[str] = None
    storage_location_id: Optional[int] = None
    is_active: bool
    version: int

    class Config:
        from_attributes = True


class QRScanRequest(BaseModel):
    token: str
    action: str
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    sample_type: Optional[str] = None
