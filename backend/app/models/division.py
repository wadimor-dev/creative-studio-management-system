from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Division(Base):
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
