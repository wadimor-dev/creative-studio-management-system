import uuid
import enum
from sqlalchemy import Column, String, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class MedicalRecordStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    FINAL = "FINAL"


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, unique=True, index=True)
    record_number = Column(String(30), unique=True, nullable=False, index=True)
    chief_complaint = Column(Text, nullable=True)
    present_illness = Column(Text, nullable=True)
    past_history = Column(Text, nullable=True)
    family_history = Column(Text, nullable=True)
    physical_exam = Column(Text, nullable=True)
    doctor_note = Column(Text, nullable=True)
    status = Column(SAEnum(MedicalRecordStatus, name="mr_status_enum", create_constraint=True, validate_strings=True), default=MedicalRecordStatus.DRAFT, nullable=False)

    visit = relationship("Visit", back_populates="medical_record")
