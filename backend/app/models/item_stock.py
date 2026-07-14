from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base

class ItemStock(Base):
    __tablename__ = "item_stocks"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    # Relationships
    item = relationship("Item", back_populates="stocks")
    location = relationship("Location")

    __table_args__ = (
        UniqueConstraint('item_id', 'location_id', name='uix_item_location_stock'),
    )
