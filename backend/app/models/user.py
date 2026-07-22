from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    must_change_password = Column(Boolean, default=True)
    password_changed_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                        onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    roles = relationship("Role", secondary="user_roles", back_populates="users", lazy="selectin")
    employee = relationship("Employee", back_populates="user", uselist=False,
                             foreign_keys="Employee.user_id")

    @property
    def full_name(self):
        try:
            if self.employee is not None:
                return self.employee.full_name
        except Exception:
            pass
        return getattr(self, '_cached_full_name', self.username)

    @full_name.setter
    def full_name(self, value):
        self._cached_full_name = value
        try:
            if self.employee:
                self.employee.full_name = value
        except Exception:
            pass
