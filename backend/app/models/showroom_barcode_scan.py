from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class ShowroomBarcodeScan(Base):
    __tablename__ = "showroom_barcode_scans"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(100), nullable=False)
    scan_type = Column(String(20), nullable=False)  # 'PRODUCT' or 'LOCATION'
    result_id = Column(Integer, nullable=True)
    result_type = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    scanned_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)

    user = relationship("User")
    location = relationship("ShowroomLocation")
