from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=True)

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles", lazy="selectin")
    users = relationship("User", secondary="user_roles", back_populates="roles", lazy="selectin")
