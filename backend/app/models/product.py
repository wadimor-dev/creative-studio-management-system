from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database.base import Base

class ProductStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISCONTINUED = "DISCONTINUED"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    
    # Master Data Foreign Keys
    type_id = Column(Integer, ForeignKey("product_types.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    motif_id = Column(Integer, ForeignKey("product_motifs.id"), nullable=False)
    sub_motif_id = Column(Integer, ForeignKey("product_sub_motifs.id"), nullable=True)
    color_id = Column(Integer, ForeignKey("product_colors.id"), nullable=True)
    
    # Custom Attributes
    variant = Column(String(100), nullable=True)  # e.g., Reguler, Jumbo, Box
    image_url = Column(String(255), nullable=True)
    
    # Generated Identities
    sku = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE, nullable=False)
    
    # Relationships
    type = relationship("ProductType")
    category = relationship("ProductCategory")
    motif = relationship("ProductMotif")
    sub_motif = relationship("ProductSubMotif")
    color = relationship("ProductColor")
