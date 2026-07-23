import uuid
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class VitalSign(Base):
    __tablename__ = "vital_signs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, unique=True, index=True)
    systolic = Column(Integer, nullable=True)
    diastolic = Column(Integer, nullable=True)
    pulse = Column(Integer, nullable=True)
    respiration = Column(Integer, nullable=True)
    temperature = Column(DECIMAL(5, 2), nullable=True)
    spo2 = Column(DECIMAL(5, 2), nullable=True)
    height = Column(DECIMAL(5, 2), nullable=True)
    weight = Column(DECIMAL(5, 2), nullable=True)
    bmi = Column(DECIMAL(5, 2), nullable=True)

    visit = relationship("Visit", back_populates="vital_sign")
