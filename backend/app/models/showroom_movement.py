from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum
from app.core.database.base import Base


class ShowroomMovementType(str, enum.Enum):
    HANDOVER = "HANDOVER"
    TRANSFER = "TRANSFER"
    BORROW = "BORROW"
    RETURN = "RETURN"
    RELEASE = "RELEASE"
    RELEASE_REJECT = "RELEASE_REJECT"
    ADJUSTMENT = "ADJUSTMENT"
    MAINTENANCE_OUT = "MAINTENANCE_OUT"
    MAINTENANCE_RETURN = "MAINTENANCE_RETURN"
    RETIRED = "RETIRED"
    SHOWROOM_IN = "SHOWROOM_IN"
    SHOWROOM_OUT = "SHOWROOM_OUT"
    RESTOCK = "RESTOCK"
    SCRAP = "SCRAP"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"


class ShowroomMovement(Base):
    __tablename__ = "showroom_movements"

    id = Column(Integer, primary_key=True, index=True)
    movement_type = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    from_location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    to_location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    sample_type = Column(String(50), nullable=True)
    purpose = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    notes = Column(String(500), nullable=True)
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    product = relationship("Product")
    from_location = relationship("ShowroomLocation", foreign_keys=[from_location_id], back_populates="movements_from")
    to_location = relationship("ShowroomLocation", foreign_keys=[to_location_id], back_populates="movements_to")
    user = relationship("User")
