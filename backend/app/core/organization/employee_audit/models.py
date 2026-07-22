from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.core.database.base import Base


class EmployeeAudit(Base):
    __tablename__ = "employee_audits"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    employee = relationship("Employee", back_populates="audits")
    changer = relationship("User", backref="employee_audits",
                            foreign_keys=[changed_by_user_id])

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
