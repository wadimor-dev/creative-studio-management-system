from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.hrd_ga.clinic.schemas import MedicalCertificateCreate, MedicalCertificateUpdate
from app.modules.hrd_ga.clinic.services import medical_certificate_service

router = APIRouter()


@router.get("/medical-certificates/{cert_id}", tags=["clinic-certificates"])
def get_certificate(cert_id: str, db: Session = Depends(get_db)):
    data = medical_certificate_service.get_by_id(db, cert_id)
    return create_success_response(data=data.model_dump())

@router.get("/medical-certificates/by-visit/{visit_id}", tags=["clinic-certificates"])
def get_certificates_by_visit(visit_id: str, db: Session = Depends(get_db)):
    items = medical_certificate_service.get_by_visit(db, visit_id)
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/medical-certificates", status_code=status.HTTP_201_CREATED, tags=["clinic-certificates"])
def create_certificate(body: MedicalCertificateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = medical_certificate_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Certificate created")

@router.put("/medical-certificates/{cert_id}", tags=["clinic-certificates"])
def update_certificate(cert_id: str, body: MedicalCertificateUpdate, db: Session = Depends(get_db)):
    data = medical_certificate_service.update(db, cert_id, body)
    return create_success_response(data=data.model_dump(), message="Certificate updated")

@router.delete("/medical-certificates/{cert_id}", tags=["clinic-certificates"])
def delete_certificate(cert_id: str, db: Session = Depends(get_db)):
    medical_certificate_service.delete(db, cert_id)
    return create_success_response(message="Certificate deleted")
