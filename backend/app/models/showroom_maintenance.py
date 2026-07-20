from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


class ShowroomMaintenance(Base):
    __tablename__ = "showroom_maintenance"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("showroom_locations.id"), nullable=True)
    maintenance_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    quantity = Column(Integer, nullable=False)
    sample_type = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    completed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    return_movement_id = Column(Integer, ForeignKey("showroom_movements.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    completed_at = Column(DateTime, nullable=True)

    product = relationship("Product")
    location = relationship("ShowroomLocation")
    creator = relationship("User", foreign_keys=[created_by])
    completer = relationship("User", foreign_keys=[completed_by])
    movement = relationship("ShowroomMovement", foreign_keys=[movement_id])
    return_movement = relationship("ShowroomMovement", foreign_keys=[return_movement_id])
