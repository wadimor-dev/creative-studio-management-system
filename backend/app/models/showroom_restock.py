from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomRestockRequest(Base):
    __tablename__ = "showroom_restock_requests"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=False)
    sample_type = Column(String(50), nullable=True)
    minimum_quantity = Column(Integer, nullable=True)
    current_quantity = Column(Integer, nullable=True)
    requested_quantity = Column(Integer, nullable=False)
    source = Column(String(20), nullable=False, default="auto")
    status = Column(String(20), nullable=False, default="PENDING")
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    product = relationship("Product")
    location = relationship("ShowroomLocation")
    requester = relationship("User", foreign_keys=[requested_by])
    approver = relationship("User", foreign_keys=[approved_by])
