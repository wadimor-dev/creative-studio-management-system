from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.patient_profile import PatientProfile
from app.modules.hrd_ga.clinic.schemas import PatientProfileCreate, PatientProfileUpdate, PatientProfileResponse


class PatientProfileService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[PatientProfileResponse]:
        query = db.query(PatientProfile).options(joinedload(PatientProfile.employee))
        if search:
            query = query.join(PatientProfile.employee).filter(
                PatientProfile.medical_record_number.ilike(f"%{search}%")
            )
        items = query.offset(skip).limit(limit).all()
        return [self._to_response(p) for p in items]

    def get_by_id(self, db: Session, patient_profile_id: str) -> PatientProfileResponse:
        patient = db.query(PatientProfile).options(joinedload(PatientProfile.employee)).filter(PatientProfile.id == patient_profile_id).first()
        if not patient:
            raise CSMSException("Patient profile not found", status_code=404)
        return self._to_response(patient)

    def get_by_employee_id(self, db: Session, employee_id: int) -> Optional[PatientProfileResponse]:
        patient = db.query(PatientProfile).options(joinedload(PatientProfile.employee)).filter(PatientProfile.employee_id == employee_id).first()
        if not patient:
            return None
        return self._to_response(patient)

    def get_by_medical_record_number(self, db: Session, mr_number: str) -> Optional[PatientProfileResponse]:
        patient = db.query(PatientProfile).options(joinedload(PatientProfile.employee)).filter(
            PatientProfile.medical_record_number == mr_number
        ).first()
        if not patient:
            return None
        return self._to_response(patient)

    def create(self, db: Session, data: PatientProfileCreate) -> PatientProfileResponse:
        existing = db.query(PatientProfile).filter(PatientProfile.medical_record_number == data.medical_record_number).first()
        if existing:
            raise CSMSException("Medical record number already exists", status_code=409)
        patient = PatientProfile(**data.model_dump())
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return self._to_response(patient)

    def update(self, db: Session, patient_profile_id: str, data: PatientProfileUpdate) -> PatientProfileResponse:
        patient = self._get_orm(db, patient_profile_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)
        db.commit()
        db.refresh(patient)
        return self._to_response(patient)

    def delete(self, db: Session, patient_profile_id: str) -> None:
        patient = self._get_orm(db, patient_profile_id)
        db.delete(patient)
        db.commit()

    def _get_orm(self, db: Session, patient_profile_id: str) -> PatientProfile:
        patient = db.query(PatientProfile).filter(PatientProfile.id == patient_profile_id).first()
        if not patient:
            raise CSMSException("Patient profile not found", status_code=404)
        return patient

    def _to_response(self, patient: PatientProfile) -> PatientProfileResponse:
        return PatientProfileResponse(
            id=patient.id,
            employee_id=patient.employee_id,
            medical_record_number=patient.medical_record_number,
            blood_type=patient.blood_type,
            rhesus=patient.rhesus,
            allergy_note=patient.allergy_note,
            emergency_contact_name=patient.emergency_contact_name,
            emergency_contact_phone=patient.emergency_contact_phone,
            created_at=patient.created_at,
            updated_at=patient.updated_at,
            created_by=patient.created_by,
            updated_by=patient.updated_by,
            employee_name=patient.employee.full_name if patient.employee else None,
        )


patient_profile_service = PatientProfileService()
