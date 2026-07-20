from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomSampleStock(Base):
    __tablename__ = "showroom_sample_stocks"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=False, index=True)
    storage_location_id = Column(Integer, ForeignKey("showroom_storage_locations.id"), nullable=True, index=True)
    sample_type = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    __table_args__ = (
        UniqueConstraint("product_id", "location_id", "sample_type", name="uix_showroom_stock_product_location_type"),
    )

    product = relationship("Product")
    location = relationship("ShowroomLocation", back_populates="stocks")
    storage_location = relationship("ShowroomStorageLocation", back_populates="stocks")
