import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class MedicineDispense(Base):
    __tablename__ = "medicine_dispenses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_item_id = Column(String(36), ForeignKey("prescription_items.id"), nullable=False, unique=True, index=True)
    dispensed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    dispensed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prescription_item = relationship("PrescriptionItem", back_populates="dispense")
