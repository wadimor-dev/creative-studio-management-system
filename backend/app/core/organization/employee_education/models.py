from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeeEducation(Base):
    __tablename__ = "employee_educations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    level = Column(String(50), nullable=False)
    institution = Column(String(200), nullable=False)
    major = Column(String(100), nullable=True)
    start_year = Column(String(4), nullable=True)
    end_year = Column(String(4), nullable=True)
    graduation_year = Column(String(4), nullable=True)
    gpa = Column(String(10), nullable=True)
    is_highest = Column(Boolean, default=False)
    certificate_number = Column(String(100), nullable=True)
    graduated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", back_populates="educations")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
