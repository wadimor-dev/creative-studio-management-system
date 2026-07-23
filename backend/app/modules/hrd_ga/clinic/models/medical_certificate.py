import uuid
import enum
from sqlalchemy import Column, String, Integer, Text, Date, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class CertificateType(str, enum.Enum):
    HEALTH = "HEALTH"
    SICK = "SICK"
    FIT_TO_WORK = "FIT_TO_WORK"


class MedicalCertificate(Base):
    __tablename__ = "medical_certificates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    certificate_type = Column(SAEnum(CertificateType, name="cert_type_enum", create_constraint=True, validate_strings=True), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    diagnosis_summary = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    issued_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    visit = relationship("Visit", back_populates="certificates")
