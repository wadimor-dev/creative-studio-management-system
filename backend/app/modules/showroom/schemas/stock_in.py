from typing import Optional, Union

from pydantic import BaseModel, field_validator


class StockInCreate(BaseModel):
    product: str
    quantity: int
    supplier: str
    location: str
    date: str
    reference: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("quantity", mode="before")
    @classmethod
    def coerce_quantity(cls, value: Union[int, str]) -> int:
        if isinstance(value, str):
            return int(value.strip()) if value.strip() else 0
        return value


class StockInUpdate(BaseModel):
    reference: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class StockInResponse(BaseModel):
    id: str
    product: dict
    quantity: int
    supplier: str
    location: str
    date: str
    status: str
    reference: Optional[str] = None
    notes: Optional[str] = None


class StockInStats(BaseModel):
    todayIn: str
    thisWeek: str
    thisMonth: str
    totalSuppliers: str
