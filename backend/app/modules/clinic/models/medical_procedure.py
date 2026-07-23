import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.core.database.base import Base


class MedicalProcedure(Base):
    __tablename__ = "medical_procedures"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    visit_procedures = relationship("VisitProcedure", back_populates="procedure", lazy="selectin")
