import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class VisitStatus(str, enum.Enum):
    CHECKIN = "CHECKIN"
    SERVING = "SERVING"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class VisitType(str, enum.Enum):
    REGULAR = "REGULAR"
    EMERGENCY = "EMERGENCY"
    FOLLOW_UP = "FOLLOW_UP"


class Visit(Base):
    __tablename__ = "visits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_number = Column(String(30), unique=True, nullable=False, index=True)
    patient_profile_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False, index=True)
    queue_id = Column(String(36), ForeignKey("queues.id"), nullable=True, unique=True)
    healthcare_professional_id = Column(String(36), ForeignKey("healthcare_professionals.id"), nullable=True, index=True)
    visit_type = Column(SAEnum(VisitType, name="visit_type_enum", create_constraint=True, validate_strings=True), default=VisitType.REGULAR, nullable=False)
    visit_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    complaint = Column(Text, nullable=True)
    visit_status = Column(SAEnum(VisitStatus, name="visit_status_enum", create_constraint=True, validate_strings=True), default=VisitStatus.CHECKIN, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    patient_profile = relationship("PatientProfile", back_populates="visits")
    queue = relationship("Queue", back_populates="visit", uselist=False)
    healthcare_professional = relationship("HealthcareProfessional", back_populates="visits")

    medical_record = relationship("MedicalRecord", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    soap_note = relationship("SOAPNote", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    vital_sign = relationship("VitalSign", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    diagnoses = relationship("Diagnosis", back_populates="visit", lazy="selectin", cascade="all, delete-orphan")
    visit_procedures = relationship("VisitProcedure", back_populates="visit", lazy="selectin", cascade="all, delete-orphan")
    prescription = relationship("Prescription", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    certificates = relationship("MedicalCertificate", back_populates="visit", lazy="selectin", cascade="all, delete-orphan")
    attachments = relationship("MedicalAttachment", back_populates="visit", lazy="selectin", cascade="all, delete-orphan")
