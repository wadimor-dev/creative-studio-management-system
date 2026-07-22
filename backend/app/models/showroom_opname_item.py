from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class ShowroomOpnameItem(Base):
    __tablename__ = "showroom_opname_items"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("showroom_opname_sessions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=False)
    expected_quantity = Column(Integer, nullable=False)
    actual_quantity = Column(Integer, nullable=True)
    variance = Column(Integer, nullable=True)
    adjustment_movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    session = relationship("ShowroomOpnameSession", back_populates="items")
    product = relationship("Product")
    location = relationship("ShowroomLocation")
    adjustment_movement = relationship("ShowroomMovement")
