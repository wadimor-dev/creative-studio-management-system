from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobLevelCreate(BaseModel):
    name: str
    code: str
    level: int = 0
    description: Optional[str] = None
    is_active: bool = True


class JobLevelUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class JobLevelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    level: int
    description: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
