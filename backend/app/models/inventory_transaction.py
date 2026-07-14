from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base
import enum
from sqlalchemy import Enum

class InventoryMovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(InventoryMovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Location tracking
    source_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    destination_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    
    # Context
    reference = Column(String(255), nullable=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), nullable=False)
    notes = Column(Text, nullable=True)

    item = relationship("Item")
    user = relationship("User")
    source_location = relationship("Location", foreign_keys=[source_location_id])
    destination_location = relationship("Location", foreign_keys=[destination_location_id])
