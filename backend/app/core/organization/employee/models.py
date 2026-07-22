from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum
from app.core.database.base import Base


class EmploymentStatus(str, enum.Enum):
    ACTIVE = "active"
    PROBATION = "probation"
    CONTRACT = "contract"
    INTERN = "intern"
    LEAVE = "leave"
    RESIGNED = "resigned"
    TERMINATED = "terminated"
    RETIRED = "retired"
    SUSPENDED = "suspended"


class EmploymentType(str, enum.Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"
    INTERN = "intern"
    OUTSOURCE = "outsource"
    PROBATION = "probation"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    employee_number = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True, index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True, index=True)
    division_id = Column(Integer, ForeignKey("divisions.id"), nullable=True, index=True)
    job_level_id = Column(Integer, ForeignKey("job_levels.id"), nullable=True, index=True)
    employment_status = Column(SAEnum(EmploymentStatus), default=EmploymentStatus.ACTIVE, nullable=False)
    employment_type = Column(SAEnum(EmploymentType), default=EmploymentType.PERMANENT, nullable=False)
    join_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None),
                        onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    deleted_at = Column(DateTime, nullable=True)
    deleted_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    delete_reason = Column(Text, nullable=True)

    user = relationship("User", back_populates="employee", uselist=False,
                         foreign_keys=[user_id])
    company = relationship("Company", backref="employees", uselist=False)
    branch = relationship("Branch", backref="employees", uselist=False)
    department = relationship("Department", backref="employees", uselist=False)
    position = relationship("Position", backref="employees", uselist=False)
    division = relationship("Division", backref="employees", uselist=False)
    job_level = relationship("JobLevel", backref="employees", uselist=False)
    deleted_by_user = relationship("User", backref="deleted_employees",
                                    foreign_keys=[deleted_by_user_id])

    personal_info = relationship("EmployeePersonalInfo", back_populates="employee", uselist=False,
                                  cascade="all, delete-orphan")
    histories = relationship("EmployeeHistory", back_populates="employee",
                              order_by="EmployeeHistory.effective_date.desc()")
    assignments = relationship("EmployeeAssignment", back_populates="employee",
                                order_by="EmployeeAssignment.start_date.desc()")
    audits = relationship("EmployeeAudit", back_populates="employee",
                           order_by="EmployeeAudit.changed_at.desc()")

    contacts = relationship("EmployeeContact", back_populates="employee",
                             cascade="all, delete-orphan")
    educations = relationship("EmployeeEducation", back_populates="employee",
                               cascade="all, delete-orphan")
    banks = relationship("EmployeeBank", back_populates="employee",
                          cascade="all, delete-orphan",
                          order_by="EmployeeBank.priority")
    emergency_contacts = relationship("EmployeeEmergencyContact", back_populates="employee",
                                       cascade="all, delete-orphan")
    families = relationship("EmployeeFamily", back_populates="employee",
                             cascade="all, delete-orphan")
    contracts = relationship("EmployeeContract", back_populates="employee",
                              cascade="all, delete-orphan",
                              order_by="EmployeeContract.start_date.desc()")
    salary_histories = relationship("EmployeeSalaryHistory", back_populates="employee",
                                     cascade="all, delete-orphan",
                                     order_by="EmployeeSalaryHistory.effective_date.desc()")
    shifts = relationship("EmployeeShift", back_populates="employee",
                           cascade="all, delete-orphan")
    assets = relationship("EmployeeAsset", back_populates="employee",
                           cascade="all, delete-orphan")
    skills = relationship("EmployeeSkill", back_populates="employee",
                           cascade="all, delete-orphan")
    certifications = relationship("EmployeeCertification", back_populates="employee",
                                   cascade="all, delete-orphan")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
