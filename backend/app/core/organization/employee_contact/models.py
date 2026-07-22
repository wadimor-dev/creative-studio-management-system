from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeeContact(Base):
    __tablename__ = "employee_contacts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    contact_type = Column(String(20), nullable=False, default="primary")
    label = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    alternate_phone = Column(String(50), nullable=True)
    current_address = Column(Text, nullable=True)
    current_province = Column(String(100), nullable=True)
    current_city = Column(String(100), nullable=True)
    current_district = Column(String(100), nullable=True)
    current_postal_code = Column(String(20), nullable=True)
    permanent_address = Column(Text, nullable=True)
    permanent_province = Column(String(100), nullable=True)
    permanent_city = Column(String(100), nullable=True)
    permanent_district = Column(String(100), nullable=True)
    permanent_postal_code = Column(String(20), nullable=True)
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                        onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", back_populates="contacts")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
