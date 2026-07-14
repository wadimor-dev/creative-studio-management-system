from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base

class ProductStock(Base):
    __tablename__ = "product_stocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    # Relationships
    product = relationship("Product")
    location = relationship("Location")

    __table_args__ = (
        UniqueConstraint('product_id', 'location_id', name='uix_product_location_stock'),
    )
