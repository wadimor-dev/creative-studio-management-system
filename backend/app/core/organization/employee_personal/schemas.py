from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmployeePersonalInfoCreate(BaseModel):
    nik: Optional[str] = None
    kk: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = "Indonesia"
    blood_type: Optional[str] = None
    photo: Optional[str] = None
    identity_number: Optional[str] = None
    tax_number: Optional[str] = None
    bpjs_kesehatan: Optional[str] = None
    bpjs_ketenagakerjaan: Optional[str] = None


class EmployeePersonalInfoUpdate(BaseModel):
    nik: Optional[str] = None
    kk: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    blood_type: Optional[str] = None
    photo: Optional[str] = None
    identity_number: Optional[str] = None
    tax_number: Optional[str] = None
    bpjs_kesehatan: Optional[str] = None
    bpjs_ketenagakerjaan: Optional[str] = None


class EmployeePersonalInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    nik: Optional[str] = None
    kk: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    religion: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    blood_type: Optional[str] = None
    photo: Optional[str] = None
    identity_number: Optional[str] = None
    tax_number: Optional[str] = None
    bpjs_kesehatan: Optional[str] = None
    bpjs_ketenagakerjaan: Optional[str] = None
