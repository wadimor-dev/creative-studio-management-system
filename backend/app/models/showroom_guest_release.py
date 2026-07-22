from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class ShowroomGuestRelease(Base):
    __tablename__ = "showroom_guest_releases"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    sample_type = Column(String(50), nullable=True)
    guest_name = Column(String(100), nullable=False)
    guest_company = Column(String(100), nullable=True)
    purpose = Column(String(255), nullable=True)
    release_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    product = relationship("Product")
    location = relationship("ShowroomLocation")
    user = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])
    rejector = relationship("User", foreign_keys=[rejected_by])
    movement = relationship("ShowroomMovement")
