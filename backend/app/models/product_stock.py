from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database.base import Base

class ProductPlacementStock(Base):
    __tablename__ = "product_placement_stocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    placement_id = Column(Integer, ForeignKey("product_placements.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)

    # Relationships
    product = relationship("Product")
    placement = relationship("ProductPlacement")

    __table_args__ = (
        UniqueConstraint('product_id', 'placement_id', name='uix_product_placement_stock'),
    )
