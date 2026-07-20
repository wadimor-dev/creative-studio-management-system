from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomReservation(Base):
    __tablename__ = "showroom_reservations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reserved_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    purpose = Column(String(255), nullable=True)
    reserved_from = Column(Date, nullable=False)
    reserved_until = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    product = relationship("Product")
    user = relationship("User")
