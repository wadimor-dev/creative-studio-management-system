from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database.base import Base

class PlacementType(Base):
    __tablename__ = "placement_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    icon = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)

class ProductPlacement(Base):
    __tablename__ = "product_placements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=True)
    name = Column(String(100), index=True, nullable=False)
    type_id = Column(Integer, ForeignKey("placement_types.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("product_placements.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    placement_type = relationship("PlacementType")
    children = relationship("ProductPlacement", backref=backref('parent', remote_side=[id]))
