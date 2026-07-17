from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


class TransferItem(BaseModel):
    product: str
    quantity: int

    @field_validator("quantity", mode="before")
    @classmethod
    def coerce_quantity(cls, value: Union[int, str]) -> int:
        if isinstance(value, str):
            return int(value.strip()) if value.strip() else 0
        return value


class TransferCreate(BaseModel):
    fromLocation: str
    toLocation: str
    items: List[TransferItem]
    estimatedArrival: str
    notes: Optional[str] = None


class TransferUpdate(BaseModel):
    estimatedArrival: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class TransferResponse(BaseModel):
    id: str
    fromLocation: str
    toLocation: str
    items: List[TransferItem]
    totalQuantity: int
    status: str
    createdAt: str
    estimatedArrival: str


class TransferStats(BaseModel):
    pendingTransfer: str
    inTransit: str
    completedToday: str
    totalThisMonth: str
