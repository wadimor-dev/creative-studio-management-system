from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomOpnameSession(Base):
    __tablename__ = "showroom_opname_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="draft")
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    completed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)

    location = relationship("ShowroomLocation")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("ShowroomOpnameItem", back_populates="session")
