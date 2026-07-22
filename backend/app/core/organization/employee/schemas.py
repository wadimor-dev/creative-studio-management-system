from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.core.organization.employee.models import EmploymentStatus, EmploymentType


class EmployeeBase(BaseModel):
    employee_number: str
    full_name: str
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    division_id: Optional[int] = None
    job_level_id: Optional[int] = None
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    employment_type: EmploymentType = EmploymentType.PERMANENT
    join_date: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(BaseModel):
    employee_number: Optional[str] = None
    full_name: Optional[str] = None
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    division_id: Optional[int] = None
    job_level_id: Optional[int] = None
    employment_status: Optional[EmploymentStatus] = None
    employment_type: Optional[EmploymentType] = None
    join_date: Optional[date] = None


class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
