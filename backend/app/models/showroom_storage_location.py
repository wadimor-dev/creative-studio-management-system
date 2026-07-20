from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomStorageLocation(Base):
    __tablename__ = "showroom_storage_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("showroom_storage_locations.id"), nullable=True, index=True)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=False, index=True)
    storage_type = Column(String(50), nullable=False, default="shelf")
    capacity_qty = Column(Integer, nullable=True)
    capacity_unit = Column(String(20), nullable=True, default="PCS")
    capacity_note = Column(String(255), nullable=True)
    used_capacity = Column(Integer, nullable=False, default=0)
    path = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    parent = relationship("ShowroomStorageLocation", remote_side=[id], backref="children")
    location = relationship("ShowroomLocation")
    stocks = relationship("ShowroomSampleStock", back_populates="storage_location")
    qr_entities = relationship("ShowroomQREntity", back_populates="storage_location")
    snapshots = relationship("ShowroomStorageSnapshot", back_populates="storage_location")
