from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base

class ProductMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"

class ProductMovementReason(str, enum.Enum):
    RECEIVE_FROM_FACTORY = "RECEIVE_FROM_FACTORY"
    SHOWROOM_TRANSFER = "SHOWROOM_TRANSFER"
    GIFT = "GIFT"
    SALES_SAMPLE = "SALES_SAMPLE"
    PHOTO_SHOOT = "PHOTO_SHOOT"
    TV_STUDIO = "TV_STUDIO"
    DAMAGED = "DAMAGED"
    MISSING = "MISSING"
    STOCK_OPNAME = "STOCK_OPNAME"
    OTHER = "OTHER"

class ProductMovement(Base):
    __tablename__ = "product_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    type = Column(Enum(ProductMovementType), nullable=False)
    reason = Column(Enum(ProductMovementReason), nullable=False, default=ProductMovementReason.OTHER)
    
    quantity = Column(Integer, nullable=False)
    
    # Placement tracking
    source_placement_id = Column(Integer, ForeignKey("product_placements.id"), nullable=True)
    destination_placement_id = Column(Integer, ForeignKey("product_placements.id"), nullable=True)
    
    # Context
    reference = Column(String(255), nullable=True) # E.g., 'Work Activity', 'Sales Form'
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    notes = Column(String(500), nullable=True)

    # User tracking
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    product = relationship("Product")
    source_placement = relationship("ProductPlacement", foreign_keys=[source_placement_id])
    destination_placement = relationship("ProductPlacement", foreign_keys=[destination_placement_id])
    user = relationship("User")
