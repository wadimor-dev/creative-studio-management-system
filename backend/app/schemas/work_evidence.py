from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.constants.work_activity import WorkEvidenceType

class WorkEvidenceBase(BaseModel):
    type: WorkEvidenceType
    description: Optional[str] = None

class WorkEvidenceCreate(WorkEvidenceBase):
    pass

class WorkEvidenceResponse(WorkEvidenceBase):
    id: int
    work_activity_id: int
    file_path: str
    file_name: str
    file_size: int
    mime_type: str
    evidence_order: int
    uploaded_by: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
