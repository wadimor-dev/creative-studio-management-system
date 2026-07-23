from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.clinic.models.diagnosis import Diagnosis
from app.modules.clinic.models.icd10_code import ICD10Code
from app.modules.clinic.schemas import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse


class DiagnosisService:

    def get_by_id(self, db: Session, diagnosis_id: str) -> DiagnosisResponse:
        diag = db.query(Diagnosis).options(
            joinedload(Diagnosis.icd10_code)
        ).filter(Diagnosis.id == diagnosis_id).first()
        if not diag:
            raise CSMSException("Diagnosis not found", status_code=404)
        return self._to_response(diag)

    def get_by_visit(self, db: Session, visit_id: str) -> List[DiagnosisResponse]:
        items = db.query(Diagnosis).options(
            joinedload(Diagnosis.icd10_code)
        ).filter(Diagnosis.visit_id == visit_id).all()
        return [self._to_response(d) for d in items]

    def create(self, db: Session, data: DiagnosisCreate) -> DiagnosisResponse:
        icd10 = db.query(ICD10Code).filter(ICD10Code.id == data.icd10_id).first()
        if not icd10:
            raise CSMSException("ICD-10 code not found", status_code=404)
        diag = Diagnosis(**data.model_dump())
        db.add(diag)
        db.commit()
        db.refresh(diag)
        return self.get_by_id(db, diag.id)

    def update(self, db: Session, diagnosis_id: str, data: DiagnosisUpdate) -> DiagnosisResponse:
        diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diag:
            raise CSMSException("Diagnosis not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(diag, field, value)
        db.commit()
        db.refresh(diag)
        return self.get_by_id(db, diag.id)

    def delete(self, db: Session, diagnosis_id: str) -> None:
        diag = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diag:
            raise CSMSException("Diagnosis not found", status_code=404)
        db.delete(diag)
        db.commit()

    def _to_response(self, diag: Diagnosis) -> DiagnosisResponse:
        return DiagnosisResponse(
            id=diag.id,
            visit_id=diag.visit_id,
            icd10_id=diag.icd10_id,
            diagnosis_type=diag.diagnosis_type,
            diagnosis_note=diag.diagnosis_note,
            icd10_code=diag.icd10_code.code if diag.icd10_code else None,
            icd10_name=diag.icd10_code.name if diag.icd10_code else None,
        )


diagnosis_service = DiagnosisService()
