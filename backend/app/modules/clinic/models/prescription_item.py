import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_id = Column(String(36), ForeignKey("prescriptions.id"), nullable=False, index=True)
    medicine_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    dosage = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=True)

    prescription = relationship("Prescription", back_populates="items")
    medicine = relationship("Item", lazy="selectin")
    dispense = relationship("MedicineDispense", back_populates="prescription_item", uselist=False, cascade="all, delete-orphan")
