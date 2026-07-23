import uuid
import enum
from sqlalchemy import Column, String, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class DiagnosisType(str, enum.Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    icd10_id = Column(String(36), ForeignKey("icd10_codes.id"), nullable=False, index=True)
    diagnosis_type = Column(SAEnum(DiagnosisType, name="diagnosis_type_enum", create_constraint=True, validate_strings=True), nullable=False)
    diagnosis_note = Column(Text, nullable=True)

    visit = relationship("Visit", back_populates="diagnoses")
    icd10_code = relationship("ICD10Code", back_populates="diagnoses")
