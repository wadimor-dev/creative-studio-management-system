
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.constants.work_activity import WorkActivityStatus

class WorkAssetPayload(BaseModel):
    item_id: int
    location_id: int
    quantity: int

class WorkAssetResponse(BaseModel):
    id: int
    item_id: int
    location_id: int
    quantity: int
    status: str
    borrowed_at: Optional[datetime]
    returned_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Category
class WorkCategoryBase(BaseModel):
    name: str

class WorkCategoryResponse(WorkCategoryBase):
    id: int
    class Config:
        from_attributes = True

# Activity
class WorkActivityBase(BaseModel):
    category_id: int
    activity_name: str
    notes: Optional[str] = None

class WorkActivityCreate(WorkActivityBase):
    pass

class WorkActivityUpdate(BaseModel):
    category_id: Optional[int] = None
    activity_name: Optional[str] = None
    notes: Optional[str] = None
    photo_before: Optional[str] = None
    photo_after: Optional[str] = None

class WorkActivityResponse(WorkActivityBase):
    id: int
    user_id: int
    status: WorkActivityStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    worked_seconds: int = 0
    current_session_started_at: Optional[datetime] = None
    photo_before: Optional[str] = None
    photo_after: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    category: Optional[WorkCategoryResponse] = None

    class Config:
        from_attributes = True


class WorkActivityStartRequest(BaseModel):
    assets: List[WorkAssetPayload] = []
