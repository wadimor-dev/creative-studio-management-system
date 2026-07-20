from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomBorrowing(Base):
    __tablename__ = "showroom_borrowings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    from_location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    borrower_name = Column(String(100), nullable=True)
    borrower_location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    sample_type = Column(String(50), nullable=True)
    purpose = Column(String(255), nullable=True)
    borrow_date = Column(Date, nullable=False)
    expected_return_date = Column(Date, nullable=True)
    actual_return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="BORROWED")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    borrowed_at = Column(DateTime, nullable=True)
    movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    return_movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    product = relationship("Product")
    from_location = relationship("ShowroomLocation", foreign_keys=[from_location_id])
    borrower_location = relationship("ShowroomLocation", foreign_keys=[borrower_location_id])
    user = relationship("User", foreign_keys=[user_id])
    movement = relationship("ShowroomMovement", foreign_keys=[movement_id])
    return_movement = relationship("ShowroomMovement", foreign_keys=[return_movement_id])
