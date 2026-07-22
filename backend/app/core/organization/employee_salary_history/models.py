from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeeSalaryHistory(Base):
    __tablename__ = "employee_salary_histories"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    basic_salary = Column(Integer, nullable=True)
    allowance_transport = Column(Integer, default=0)
    allowance_meal = Column(Integer, default=0)
    allowance_position = Column(Integer, default=0)
    allowance_communication = Column(Integer, default=0)
    overtime_rate = Column(Integer, nullable=True)
    salary_grade = Column(String(50), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", back_populates="salary_histories")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
