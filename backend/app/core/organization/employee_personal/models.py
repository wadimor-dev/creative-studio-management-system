from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeePersonalInfo(Base):
    __tablename__ = "employee_personal_infos"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True, index=True)
    nik = Column(String(20), nullable=True)
    kk = Column(String(30), nullable=True)
    gender = Column(String(10), nullable=True)
    birth_place = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    religion = Column(String(50), nullable=True)
    marital_status = Column(String(20), nullable=True)
    nationality = Column(String(50), nullable=True, default="Indonesia")
    blood_type = Column(String(5), nullable=True)
    photo = Column(String(500), nullable=True)
    identity_number = Column(String(50), nullable=True)
    tax_number = Column(String(50), nullable=True)
    bpjs_kesehatan = Column(String(50), nullable=True)
    bpjs_ketenagakerjaan = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                        onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", back_populates="personal_info", uselist=False)

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
