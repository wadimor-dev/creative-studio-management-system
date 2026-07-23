import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class PrescriptionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DISPENSED = "DISPENSED"
    CANCELLED = "CANCELLED"


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, unique=True, index=True)
    healthcare_professional_id = Column(String(36), ForeignKey("healthcare_professionals.id"), nullable=True, index=True)
    prescription_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(SAEnum(PrescriptionStatus, name="rx_status_enum", create_constraint=True, validate_strings=True), default=PrescriptionStatus.ACTIVE, nullable=False)

    visit = relationship("Visit", back_populates="prescription")
    items = relationship("PrescriptionItem", back_populates="prescription", lazy="selectin", cascade="all, delete-orphan")
