from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomStorageSnapshot(Base):
    __tablename__ = "showroom_storage_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    storage_location_id = Column(Integer, ForeignKey("showroom_storage_locations.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    sample_type = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    snapshot_type = Column(String(30), nullable=False, default="NIGHTLY")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    storage_location = relationship("ShowroomStorageLocation", back_populates="snapshots")
    product = relationship("Product")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
