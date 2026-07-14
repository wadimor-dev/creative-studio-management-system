from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
