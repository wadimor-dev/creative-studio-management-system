from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    stock_qty = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    category = relationship("Category")
    unit = relationship("Unit")
    location = relationship("Location")
    stocks = relationship("ItemStock", back_populates="item", cascade="all, delete-orphan")
