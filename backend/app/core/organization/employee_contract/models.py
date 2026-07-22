from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeeContract(Base):
    __tablename__ = "employee_contracts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    contract_number = Column(String(50), unique=True, index=True, nullable=False)
    contract_type = Column(String(50), nullable=False, default="pkwt")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    basic_salary = Column(Integer, nullable=True)
    document_file = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    signed_by_employee = Column(Boolean, default=False)
    signed_by_company = Column(Boolean, default=False)
    signed_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                        onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", back_populates="contracts")
    position = relationship("Position", backref="employee_contracts")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
