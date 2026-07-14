from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base

class WorkAsset(Base):
    __tablename__ = "work_assets"

    id = Column(Integer, primary_key=True, index=True)
    work_activity_id = Column(Integer, ForeignKey("work_activities.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="BORROWED") # BORROWED, RETURNED
    
    borrowed_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)

    activity = relationship("WorkActivity", back_populates="assets")
    item = relationship("Item")
    location = relationship("Location")
