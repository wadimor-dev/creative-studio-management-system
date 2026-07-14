from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.item import ItemResponse
from app.schemas.user import UserResponse

from app.models.inventory_transaction import InventoryMovementType
from app.schemas.location import LocationResponse

class TransactionBase(BaseModel):
    item_id: int
    quantity: int
    type: InventoryMovementType
    source_location_id: Optional[int] = None
    destination_location_id: Optional[int] = None
    reference: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    
    item: Optional[ItemResponse] = None
    user: Optional[UserResponse] = None
    source_location: Optional[LocationResponse] = None
    destination_location: Optional[LocationResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
