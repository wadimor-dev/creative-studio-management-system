from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.clinic.schemas import (
    MedicalRecordCreate, MedicalRecordUpdate,
    SOAPNoteCreate, SOAPNoteUpdate,
    VitalSignCreate, VitalSignUpdate,
    DiagnosisCreate, DiagnosisUpdate,
    VisitProcedureCreate, VisitProcedureUpdate,
    MedicalAttachmentCreate, MedicalAttachmentUpdate,
)
from app.modules.clinic.services import (
    medical_record_service, soap_note_service, vital_sign_service,
    diagnosis_service, visit_procedure_service, medical_attachment_service,
)

router = APIRouter()


# ──────── MEDICAL RECORDS ────────

@router.get("/medical-records", tags=["clinic-medical-records"])
def list_medical_records(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    items = medical_record_service.get_all(db, skip=(page - 1) * size, limit=size)
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/medical-records/{record_id}", tags=["clinic-medical-records"])
def get_medical_record(record_id: str, db: Session = Depends(get_db)):
    data = medical_record_service.get_by_id(db, record_id)
    return create_success_response(data=data.model_dump())

@router.get("/medical-records/by-visit/{visit_id}", tags=["clinic-medical-records"])
def get_medical_record_by_visit(visit_id: str, db: Session = Depends(get_db)):
    data = medical_record_service.get_by_visit_id(db, visit_id)
    return create_success_response(data=data.model_dump() if data else None)

@router.post("/medical-records", status_code=status.HTTP_201_CREATED, tags=["clinic-medical-records"])
def create_medical_record(body: MedicalRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = medical_record_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Medical record created")

@router.put("/medical-records/{record_id}", tags=["clinic-medical-records"])
def update_medical_record(record_id: str, body: MedicalRecordUpdate, db: Session = Depends(get_db)):
    data = medical_record_service.update(db, record_id, body)
    return create_success_response(data=data.model_dump(), message="Medical record updated")

@router.put("/medical-records/{record_id}/finalize", tags=["clinic-medical-records"])
def finalize_medical_record(record_id: str, db: Session = Depends(get_db)):
    data = medical_record_service.finalize(db, record_id)
    return create_success_response(data=data.model_dump(), message="Medical record finalized")


# ──────── SOAP NOTES ────────

@router.get("/soap-notes/{note_id}", tags=["clinic-soap"])
def get_soap_note(note_id: str, db: Session = Depends(get_db)):
    data = soap_note_service.get_by_id(db, note_id)
    return create_success_response(data=data.model_dump())

@router.get("/soap-notes/by-visit/{visit_id}", tags=["clinic-soap"])
def get_soap_by_visit(visit_id: str, db: Session = Depends(get_db)):
    data = soap_note_service.get_by_visit_id(db, visit_id)
    return create_success_response(data=data.model_dump() if data else None)

@router.post("/soap-notes", status_code=status.HTTP_201_CREATED, tags=["clinic-soap"])
def create_soap_note(body: SOAPNoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = soap_note_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="SOAP note created")

@router.put("/soap-notes/{note_id}", tags=["clinic-soap"])
def update_soap_note(note_id: str, body: SOAPNoteUpdate, db: Session = Depends(get_db)):
    data = soap_note_service.update(db, note_id, body)
    return create_success_response(data=data.model_dump(), message="SOAP note updated")

@router.put("/soap-notes/by-visit/{visit_id}", tags=["clinic-soap"])
def upsert_soap_note(visit_id: str, body: SOAPNoteUpdate, db: Session = Depends(get_db)):
    data = soap_note_service.upsert(db, visit_id, body)
    return create_success_response(data=data.model_dump(), message="SOAP note saved")


# ──────── VITAL SIGNS ────────

@router.get("/vital-signs/{vs_id}", tags=["clinic-vitals"])
def get_vital_sign(vs_id: str, db: Session = Depends(get_db)):
    data = vital_sign_service.get_by_id(db, vs_id)
    return create_success_response(data=data.model_dump())

@router.get("/vital-signs/by-visit/{visit_id}", tags=["clinic-vitals"])
def get_vitals_by_visit(visit_id: str, db: Session = Depends(get_db)):
    data = vital_sign_service.get_by_visit_id(db, visit_id)
    return create_success_response(data=data.model_dump() if data else None)

@router.post("/vital-signs", status_code=status.HTTP_201_CREATED, tags=["clinic-vitals"])
def create_vital_sign(body: VitalSignCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = vital_sign_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Vital signs recorded")

@router.put("/vital-signs/{vs_id}", tags=["clinic-vitals"])
def update_vital_sign(vs_id: str, body: VitalSignUpdate, db: Session = Depends(get_db)):
    data = vital_sign_service.update(db, vs_id, body)
    return create_success_response(data=data.model_dump(), message="Vital signs updated")

@router.put("/vital-signs/by-visit/{visit_id}", tags=["clinic-vitals"])
def upsert_vital_sign(visit_id: str, body: VitalSignUpdate, db: Session = Depends(get_db)):
    data = vital_sign_service.upsert(db, visit_id, body)
    return create_success_response(data=data.model_dump(), message="Vital signs saved")


# ──────── DIAGNOSES ────────

@router.get("/diagnoses/by-visit/{visit_id}", tags=["clinic-diagnoses"])
def get_diagnoses_by_visit(visit_id: str, db: Session = Depends(get_db)):
    items = diagnosis_service.get_by_visit(db, visit_id)
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/diagnoses", status_code=status.HTTP_201_CREATED, tags=["clinic-diagnoses"])
def create_diagnosis(body: DiagnosisCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = diagnosis_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Diagnosis added")

@router.put("/diagnoses/{diagnosis_id}", tags=["clinic-diagnoses"])
def update_diagnosis(diagnosis_id: str, body: DiagnosisUpdate, db: Session = Depends(get_db)):
    data = diagnosis_service.update(db, diagnosis_id, body)
    return create_success_response(data=data.model_dump(), message="Diagnosis updated")

@router.delete("/diagnoses/{diagnosis_id}", tags=["clinic-diagnoses"])
def delete_diagnosis(diagnosis_id: str, db: Session = Depends(get_db)):
    diagnosis_service.delete(db, diagnosis_id)
    return create_success_response(message="Diagnosis removed")


# ──────── VISIT PROCEDURES ────────

@router.get("/visit-procedures/by-visit/{visit_id}", tags=["clinic-visit-procedures"])
def get_procedures_by_visit(visit_id: str, db: Session = Depends(get_db)):
    items = visit_procedure_service.get_by_visit(db, visit_id)
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/visit-procedures", status_code=status.HTTP_201_CREATED, tags=["clinic-visit-procedures"])
def create_visit_procedure(body: VisitProcedureCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = visit_procedure_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Procedure added to visit")

@router.put("/visit-procedures/{vp_id}", tags=["clinic-visit-procedures"])
def update_visit_procedure(vp_id: str, body: VisitProcedureUpdate, db: Session = Depends(get_db)):
    data = visit_procedure_service.update(db, vp_id, body)
    return create_success_response(data=data.model_dump(), message="Procedure updated")

@router.delete("/visit-procedures/{vp_id}", tags=["clinic-visit-procedures"])
def delete_visit_procedure(vp_id: str, db: Session = Depends(get_db)):
    visit_procedure_service.delete(db, vp_id)
    return create_success_response(message="Procedure removed from visit")


# ──────── MEDICAL ATTACHMENTS ────────

@router.get("/medical-attachments/by-visit/{visit_id}", tags=["clinic-attachments"])
def get_attachments_by_visit(visit_id: str, db: Session = Depends(get_db)):
    items = medical_attachment_service.get_by_visit(db, visit_id)
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/medical-attachments", status_code=status.HTTP_201_CREATED, tags=["clinic-attachments"])
def create_attachment(body: MedicalAttachmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = medical_attachment_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Attachment added")

@router.put("/medical-attachments/{att_id}", tags=["clinic-attachments"])
def update_attachment(att_id: str, body: MedicalAttachmentUpdate, db: Session = Depends(get_db)):
    data = medical_attachment_service.update(db, att_id, body)
    return create_success_response(data=data.model_dump(), message="Attachment updated")

@router.delete("/medical-attachments/{att_id}", tags=["clinic-attachments"])
def delete_attachment(att_id: str, db: Session = Depends(get_db)):
    medical_attachment_service.delete(db, att_id)
    return create_success_response(message="Attachment deleted")
