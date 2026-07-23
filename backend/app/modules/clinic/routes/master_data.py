from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.clinic.schemas import (
    PatientProfileCreate, PatientProfileUpdate, PatientProfileResponse,
    HealthcareProfessionalCreate, HealthcareProfessionalUpdate, HealthcareProfessionalResponse,
    ICD10CodeCreate, ICD10CodeUpdate, ICD10CodeResponse,
    MedicalProcedureCreate, MedicalProcedureUpdate, MedicalProcedureResponse,
    Profession, ProfessionalStatus,
)
from app.modules.clinic.services import (
    patient_profile_service, healthcare_professional_service,
    icd10_code_service, medical_procedure_service,
)

router = APIRouter()


# ──────── PATIENTS ────────

@router.get("/patients", tags=["clinic-patients"])
def list_patients(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = patient_profile_service.get_all(db, skip=(page - 1) * size, limit=size, search=search)
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/patients/{patient_id}", tags=["clinic-patients"])
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    data = patient_profile_service.get_by_id(db, patient_id)
    return create_success_response(data=data.model_dump())

@router.get("/patients/by-employee/{employee_id}", tags=["clinic-patients"])
def get_patient_by_employee(employee_id: int, db: Session = Depends(get_db)):
    data = patient_profile_service.get_by_employee_id(db, employee_id)
    if not data:
        return create_success_response(data=None, message="Patient not found")
    return create_success_response(data=data.model_dump())

@router.get("/patients/by-mr/{mr_number}", tags=["clinic-patients"])
def get_patient_by_mr(mr_number: str, db: Session = Depends(get_db)):
    data = patient_profile_service.get_by_medical_record_number(db, mr_number)
    if not data:
        return create_success_response(data=None, message="Patient not found")
    return create_success_response(data=data.model_dump())

@router.post("/patients", status_code=status.HTTP_201_CREATED, tags=["clinic-patients"])
def create_patient(body: PatientProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = patient_profile_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Patient created successfully")

@router.put("/patients/{patient_id}", tags=["clinic-patients"])
def update_patient(patient_id: str, body: PatientProfileUpdate, db: Session = Depends(get_db)):
    data = patient_profile_service.update(db, patient_id, body)
    return create_success_response(data=data.model_dump(), message="Patient updated successfully")

@router.delete("/patients/{patient_id}", tags=["clinic-patients"])
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient_profile_service.delete(db, patient_id)
    return create_success_response(message="Patient deleted successfully")


# ──────── HEALTHCARE PROFESSIONALS ────────

@router.get("/healthcare-professionals", tags=["clinic-hp"])
def list_hp(
    profession: Profession | None = Query(None),
    status: ProfessionalStatus | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = healthcare_professional_service.get_all(
        db, profession=profession, status=status, skip=(page - 1) * size, limit=size
    )
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/healthcare-professionals/{hp_id}", tags=["clinic-hp"])
def get_hp(hp_id: str, db: Session = Depends(get_db)):
    data = healthcare_professional_service.get_by_id(db, hp_id)
    return create_success_response(data=data.model_dump())

@router.post("/healthcare-professionals", status_code=status.HTTP_201_CREATED, tags=["clinic-hp"])
def create_hp(body: HealthcareProfessionalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = healthcare_professional_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Healthcare professional created successfully")

@router.put("/healthcare-professionals/{hp_id}", tags=["clinic-hp"])
def update_hp(hp_id: str, body: HealthcareProfessionalUpdate, db: Session = Depends(get_db)):
    data = healthcare_professional_service.update(db, hp_id, body)
    return create_success_response(data=data.model_dump(), message="Updated successfully")

@router.delete("/healthcare-professionals/{hp_id}", tags=["clinic-hp"])
def delete_hp(hp_id: str, db: Session = Depends(get_db)):
    healthcare_professional_service.delete(db, hp_id)
    return create_success_response(message="Deleted successfully")


# ──────── ICD-10 CODES ────────

@router.get("/icd10-codes", tags=["clinic-icd10"])
def list_icd10(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = icd10_code_service.get_all(db, search=search, skip=(page - 1) * size, limit=size)
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/icd10-codes/{code_id}", tags=["clinic-icd10"])
def get_icd10(code_id: str, db: Session = Depends(get_db)):
    data = icd10_code_service.get_by_id(db, code_id)
    return create_success_response(data=data.model_dump())

@router.post("/icd10-codes", status_code=status.HTTP_201_CREATED, tags=["clinic-icd10"])
def create_icd10(body: ICD10CodeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = icd10_code_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="ICD-10 code created successfully")

@router.put("/icd10-codes/{code_id}", tags=["clinic-icd10"])
def update_icd10(code_id: str, body: ICD10CodeUpdate, db: Session = Depends(get_db)):
    data = icd10_code_service.update(db, code_id, body)
    return create_success_response(data=data.model_dump(), message="Updated successfully")

@router.delete("/icd10-codes/{code_id}", tags=["clinic-icd10"])
def delete_icd10(code_id: str, db: Session = Depends(get_db)):
    icd10_code_service.delete(db, code_id)
    return create_success_response(message="Deleted successfully")


# ──────── MEDICAL PROCEDURES ────────

@router.get("/medical-procedures", tags=["clinic-procedures"])
def list_procedures(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = medical_procedure_service.get_all(db, search=search, skip=(page - 1) * size, limit=size)
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/medical-procedures/{proc_id}", tags=["clinic-procedures"])
def get_procedure(proc_id: str, db: Session = Depends(get_db)):
    data = medical_procedure_service.get_by_id(db, proc_id)
    return create_success_response(data=data.model_dump())

@router.post("/medical-procedures", status_code=status.HTTP_201_CREATED, tags=["clinic-procedures"])
def create_procedure(body: MedicalProcedureCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = medical_procedure_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Procedure created successfully")

@router.put("/medical-procedures/{proc_id}", tags=["clinic-procedures"])
def update_procedure(proc_id: str, body: MedicalProcedureUpdate, db: Session = Depends(get_db)):
    data = medical_procedure_service.update(db, proc_id, body)
    return create_success_response(data=data.model_dump(), message="Updated successfully")

@router.delete("/medical-procedures/{proc_id}", tags=["clinic-procedures"])
def delete_procedure(proc_id: str, db: Session = Depends(get_db)):
    medical_procedure_service.delete(db, proc_id)
    return create_success_response(message="Deleted successfully")
