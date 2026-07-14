from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    division_id = Column(Integer, ForeignKey("divisions.id"), nullable=True)

    role = relationship("Role", backref="users")
    division = relationship("Division", backref="users")
