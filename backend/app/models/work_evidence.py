from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.constants.work_activity import WorkEvidenceType
from app.database.base import Base

class WorkEvidence(Base):
    __tablename__ = "work_evidences"

    id = Column(Integer, primary_key=True, index=True)
    work_activity_id = Column(Integer, ForeignKey("work_activities.id"), nullable=False)
    type = Column(Enum(WorkEvidenceType), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    evidence_order = Column(Integer, default=1, nullable=False)
    
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    
    activity = relationship("WorkActivity", back_populates="evidences")
    uploader = relationship("User")
