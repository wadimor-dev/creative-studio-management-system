from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.exceptions import CSMSException
from app.modules.clinic.models.medical_certificate import MedicalCertificate
from app.modules.clinic.schemas import MedicalCertificateCreate, MedicalCertificateUpdate, MedicalCertificateResponse


class MedicalCertificateService:

    def get_by_id(self, db: Session, cert_id: str) -> MedicalCertificateResponse:
        cert = db.query(MedicalCertificate).filter(MedicalCertificate.id == cert_id).first()
        if not cert:
            raise CSMSException("Certificate not found", status_code=404)
        return MedicalCertificateResponse.model_validate(cert)

    def get_by_visit(self, db: Session, visit_id: str) -> List[MedicalCertificateResponse]:
        items = db.query(MedicalCertificate).filter(MedicalCertificate.visit_id == visit_id).all()
        return [MedicalCertificateResponse.model_validate(c) for c in items]

    def create(self, db: Session, data: MedicalCertificateCreate) -> MedicalCertificateResponse:
        cert = MedicalCertificate(**data.model_dump())
        db.add(cert)
        db.commit()
        db.refresh(cert)
        return MedicalCertificateResponse.model_validate(cert)

    def update(self, db: Session, cert_id: str, data: MedicalCertificateUpdate) -> MedicalCertificateResponse:
        cert = db.query(MedicalCertificate).filter(MedicalCertificate.id == cert_id).first()
        if not cert:
            raise CSMSException("Certificate not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cert, field, value)
        db.commit()
        db.refresh(cert)
        return MedicalCertificateResponse.model_validate(cert)

    def delete(self, db: Session, cert_id: str) -> None:
        cert = db.query(MedicalCertificate).filter(MedicalCertificate.id == cert_id).first()
        if not cert:
            raise CSMSException("Certificate not found", status_code=404)
        db.delete(cert)
        db.commit()


medical_certificate_service = MedicalCertificateService()
