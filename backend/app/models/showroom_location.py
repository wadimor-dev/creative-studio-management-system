from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomLocation(Base):
    __tablename__ = "showroom_locations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 'internal' or 'external'
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    stocks = relationship("ShowroomSampleStock", back_populates="location")
    movements_from = relationship("ShowroomMovement", foreign_keys="ShowroomMovement.from_location_id", back_populates="from_location")
    movements_to = relationship("ShowroomMovement", foreign_keys="ShowroomMovement.to_location_id", back_populates="to_location")
