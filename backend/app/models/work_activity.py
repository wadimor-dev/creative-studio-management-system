from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.constants.work_activity import WorkActivityStatus
from app.database.base import Base

class WorkActivity(Base):
    __tablename__ = "work_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("work_categories.id"), nullable=False)
    activity_name = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(Enum(WorkActivityStatus), default=WorkActivityStatus.READY, nullable=False)
    
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    worked_seconds = Column(Integer, default=0, nullable=False)
    current_session_started_at = Column(DateTime, nullable=True)
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    category = relationship("WorkCategory")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    
    evidences = relationship("WorkEvidence", back_populates="activity")
    assets = relationship("WorkAsset", back_populates="activity")
