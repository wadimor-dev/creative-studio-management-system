import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class BloodType(str, enum.Enum):
    A = "A"
    B = "B"
    AB = "AB"
    O = "O"


class Rhesus(str, enum.Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True, index=True)
    medical_record_number = Column(String(30), unique=True, nullable=False, index=True)
    blood_type = Column(SAEnum(BloodType, name="blood_type_enum", create_constraint=True, validate_strings=True), nullable=True)
    rhesus = Column(SAEnum(Rhesus, name="rhesus_enum", create_constraint=True, validate_strings=True), nullable=True)
    allergy_note = Column(Text, nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(30), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    employee = relationship("Employee", backref="patient_profile", uselist=False)
    visits = relationship("Visit", back_populates="patient_profile", lazy="selectin")
