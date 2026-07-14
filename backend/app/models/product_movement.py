from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone, timedelta
from app.database.base import Base

class ProductMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"

class ProductMovement(Base):
    __tablename__ = "product_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    type = Column(Enum(ProductMovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Location tracking
    source_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    destination_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    
    # Context
    reference = Column(String(255), nullable=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    notes = Column(String(500), nullable=True)

    # User tracking
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    product = relationship("Product")
    source_location = relationship("Location", foreign_keys=[source_location_id])
    destination_location = relationship("Location", foreign_keys=[destination_location_id])
    user = relationship("User")
