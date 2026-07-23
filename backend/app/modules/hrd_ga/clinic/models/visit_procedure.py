import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class VisitProcedure(Base):
    __tablename__ = "visit_procedures"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    procedure_id = Column(String(36), ForeignKey("medical_procedures.id"), nullable=False, index=True)
    notes = Column(Text, nullable=True)

    visit = relationship("Visit", back_populates="visit_procedures")
    procedure = relationship("MedicalProcedure", back_populates="visit_procedures")
