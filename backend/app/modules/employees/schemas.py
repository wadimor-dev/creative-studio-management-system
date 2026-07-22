from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from app.core.organization.employee.models import EmploymentStatus, EmploymentType


class EmployeeFamilyCreate(BaseModel):
    name: str
    relationship: str
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    occupation: Optional[str] = None
    phone: Optional[str] = None
    is_dependent: bool = False
    is_emergency_contact: bool = False


class EmployeeBankCreate(BaseModel):
    bank_id: Optional[int] = None
    account_number: Optional[str] = None
    account_holder: Optional[str] = None
    branch_name: Optional[str] = None
    is_payroll: bool = False
    priority: int = 1


class EmployeeEmergencyContactCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    relation: Optional[str] = None
    is_primary: bool = False


class EmployeeContactCreate(BaseModel):
    contact_type: str = "primary"
    label: Optional[str] = None
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    current_address: Optional[str] = None
    current_province: Optional[str] = None
    current_city: Optional[str] = None
    current_district: Optional[str] = None
    current_postal_code: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_province: Optional[str] = None
    permanent_city: Optional[str] = None
    permanent_district: Optional[str] = None
    permanent_postal_code: Optional[str] = None
    is_primary: bool = False


class EmployeeEducationCreate(BaseModel):
    level: str = ""
    institution: str = ""
    major: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None
    is_highest: bool = True
    certificate_number: Optional[str] = None
    graduated: bool = True


class EmployeeCreate(BaseModel):
    user_id: int
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

    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    current_address: Optional[str] = None
    current_province: Optional[str] = None
    current_city: Optional[str] = None
    current_district: Optional[str] = None
    current_postal_code: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_province: Optional[str] = None
    permanent_city: Optional[str] = None
    permanent_district: Optional[str] = None
    permanent_postal_code: Optional[str] = None

    education_level: Optional[str] = None
    education_institution: Optional[str] = None
    education_major: Optional[str] = None
    education_start_year: Optional[str] = None
    education_end_year: Optional[str] = None
    education_graduation_year: Optional[str] = None
    education_certificate_number: Optional[str] = None
    education_graduated: bool = True

    bank_id: Optional[int] = None
    bank_account: Optional[str] = None
    bank_account_holder: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

    contacts: Optional[List[EmployeeContactCreate]] = None
    banks: Optional[List[EmployeeBankCreate]] = None
    emergency_contacts: Optional[List[EmployeeEmergencyContactCreate]] = None
    families: Optional[List[EmployeeFamilyCreate]] = None


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

    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    current_address: Optional[str] = None
    current_province: Optional[str] = None
    current_city: Optional[str] = None
    current_district: Optional[str] = None
    current_postal_code: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_province: Optional[str] = None
    permanent_city: Optional[str] = None
    permanent_district: Optional[str] = None
    permanent_postal_code: Optional[str] = None

    education_level: Optional[str] = None
    education_institution: Optional[str] = None
    education_major: Optional[str] = None
    education_start_year: Optional[str] = None
    education_end_year: Optional[str] = None
    education_graduation_year: Optional[str] = None
    education_certificate_number: Optional[str] = None
    education_graduated: Optional[bool] = None

    bank_id: Optional[int] = None
    bank_account: Optional[str] = None
    bank_account_holder: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None


class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    employee_number: str
    full_name: str
    username: Optional[str] = None
    email: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    position_id: Optional[int] = None
    position_name: Optional[str] = None
    division_id: Optional[int] = None
    division_name: Optional[str] = None
    job_level_id: Optional[int] = None
    job_level_name: Optional[str] = None
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    employment_type: EmploymentType = EmploymentType.PERMANENT
    join_date: Optional[date] = None

    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    current_address: Optional[str] = None
    current_province: Optional[str] = None
    current_city: Optional[str] = None
    current_district: Optional[str] = None
    current_postal_code: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_province: Optional[str] = None
    permanent_city: Optional[str] = None
    permanent_district: Optional[str] = None
    permanent_postal_code: Optional[str] = None

    education_level: Optional[str] = None
    education_institution: Optional[str] = None
    education_major: Optional[str] = None
    education_start_year: Optional[str] = None
    education_end_year: Optional[str] = None
    education_graduation_year: Optional[str] = None
    education_certificate_number: Optional[str] = None
    education_graduated: Optional[bool] = None

    bank_id: Optional[int] = None
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    bank_account_holder: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

    deleted_at: Optional[str] = None

    class Config:
        from_attributes = True
