from typing import Optional

from pydantic import BaseModel


class ShowroomStockStats(BaseModel):
    totalStock: str
    stockInToday: str
    stockOutToday: str
    pendingTransfer: str
    stockInCount: str
    stockOutCount: str
    inTransit: str


class ShowroomStockMovement(BaseModel):
    id: str
    product: dict
    type: str
    quantity: int
    location: str
    date: str
    status: str
    reference: Optional[str] = None
