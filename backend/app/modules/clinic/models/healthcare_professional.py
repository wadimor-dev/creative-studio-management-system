import uuid
import enum
from sqlalchemy import Column, String, Integer, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class Profession(str, enum.Enum):
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    MIDWIFE = "MIDWIFE"
    LAB_TECHNICIAN = "LAB_TECHNICIAN"
    PHARMACIST = "PHARMACIST"
    DENTIST = "DENTIST"
    OTHER = "OTHER"


class ProfessionalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class HealthcareProfessional(Base):
    __tablename__ = "healthcare_professionals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True, index=True)
    profession = Column(SAEnum(Profession, name="profession_enum", create_constraint=True, validate_strings=True), nullable=False)
    specialization = Column(String(100), nullable=True)
    license_number = Column(String(50), nullable=True, index=True)
    status = Column(SAEnum(ProfessionalStatus, name="prof_status_enum", create_constraint=True, validate_strings=True), default=ProfessionalStatus.ACTIVE, nullable=False)

    employee = relationship("Employee", backref="healthcare_professional", uselist=False)
    visits = relationship("Visit", back_populates="healthcare_professional", lazy="selectin")
