import uuid
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)

    diagnoses = relationship("Diagnosis", back_populates="icd10_code", lazy="selectin")
