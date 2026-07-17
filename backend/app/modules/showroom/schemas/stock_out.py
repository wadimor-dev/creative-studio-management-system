from typing import Optional, Union

from pydantic import BaseModel, field_validator


class StockOutCreate(BaseModel):
    product: str
    quantity: int
    customer: str
    location: str
    date: str
    reference: Optional[str] = None
    reason: str
    notes: Optional[str] = None

    @field_validator("quantity", mode="before")
    @classmethod
    def coerce_quantity(cls, value: Union[int, str]) -> int:
        if isinstance(value, str):
            return int(value.strip()) if value.strip() else 0
        return value


class StockOutUpdate(BaseModel):
    reference: Optional[str] = None
    notes: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None


class StockOutResponse(BaseModel):
    id: str
    product: dict
    quantity: int
    customer: str
    location: str
    date: str
    status: str
    reference: Optional[str] = None
    reason: str
    notes: Optional[str] = None


class StockOutStats(BaseModel):
    todayOut: str
    thisWeek: str
    thisMonth: str
    totalCustomers: str
