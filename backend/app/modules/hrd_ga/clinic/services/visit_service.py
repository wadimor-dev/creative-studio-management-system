from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.visit import Visit, VisitStatus
from app.modules.hrd_ga.clinic.models.patient_profile import PatientProfile
from app.modules.hrd_ga.clinic.models.queue import Queue, QueueStatus
from app.modules.hrd_ga.clinic.models.healthcare_professional import HealthcareProfessional
from app.modules.hrd_ga.clinic.schemas import VisitCreate, VisitUpdate, VisitResponse, VisitDetailResponse


class VisitService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                patient_profile_id: Optional[str] = None,
                status: Optional[VisitStatus] = None,
                visit_date_from: Optional[datetime] = None,
                visit_date_to: Optional[datetime] = None) -> List[VisitResponse]:
        query = db.query(Visit).options(
            joinedload(Visit.patient_profile).joinedload(PatientProfile.employee),
            joinedload(Visit.healthcare_professional).joinedload(HealthcareProfessional.employee),
            joinedload(Visit.queue),
        )
        if patient_profile_id:
            query = query.filter(Visit.patient_profile_id == patient_profile_id)
        if status:
            query = query.filter(Visit.visit_status == status)
        if visit_date_from:
            query = query.filter(Visit.visit_date >= visit_date_from)
        if visit_date_to:
            query = query.filter(Visit.visit_date <= visit_date_to)
        items = query.order_by(Visit.visit_date.desc()).offset(skip).limit(limit).all()
        return [self._to_response(v) for v in items]

    def get_by_id(self, db: Session, visit_id: str) -> VisitResponse:
        visit = self._get_visit_with_relations(db, visit_id)
        return self._to_response(visit)

    def get_detail(self, db: Session, visit_id: str) -> VisitDetailResponse:
        visit = self._get_visit_with_relations(db, visit_id)
        base = self._to_response(visit)

        from app.modules.hrd_ga.clinic.services.medical_record_service import medical_record_service
        from app.modules.hrd_ga.clinic.services.soap_note_service import soap_note_service
        from app.modules.hrd_ga.clinic.services.vital_sign_service import vital_sign_service
        from app.modules.hrd_ga.clinic.services.diagnosis_service import diagnosis_service
        from app.modules.hrd_ga.clinic.services.visit_procedure_service import visit_procedure_service
        from app.modules.hrd_ga.clinic.services.prescription_service import prescription_service
        from app.modules.hrd_ga.clinic.services.medical_certificate_service import medical_certificate_service
        from app.modules.hrd_ga.clinic.services.medical_attachment_service import medical_attachment_service

        mr = medical_record_service.get_by_visit_id(db, visit_id) if visit.medical_record else None
        soap = soap_note_service.get_by_visit_id(db, visit_id) if visit.soap_note else None
        vs = vital_sign_service.get_by_visit_id(db, visit_id) if visit.vital_sign else None
        diagnoses = diagnosis_service.get_by_visit(db, visit_id) if visit.diagnoses else []
        procedures = visit_procedure_service.get_by_visit(db, visit_id) if visit.visit_procedures else []
        rx = prescription_service.get_by_visit_id(db, visit_id) if visit.prescription else None
        certs = [medical_certificate_service.get_by_id(db, c.id) for c in (visit.certificates or [])]
        atts = [medical_attachment_service.get_by_id(db, a.id) for a in (visit.attachments or [])]

        return VisitDetailResponse(
            **base.model_dump(),
            medical_record=mr,
            soap_note=soap,
            vital_sign=vs,
            diagnoses=diagnoses or [],
            procedures=procedures or [],
            prescription=rx,
            certificates=certs or [],
            attachments=atts or [],
        )

    def get_by_patient_profile(self, db: Session, patient_profile_id: str, limit: int = 10) -> List[VisitResponse]:
        visits = db.query(Visit).options(
            joinedload(Visit.patient_profile).joinedload(PatientProfile.employee),
            joinedload(Visit.healthcare_professional).joinedload(HealthcareProfessional.employee),
            joinedload(Visit.queue),
        ).filter(Visit.patient_profile_id == patient_profile_id).order_by(Visit.visit_date.desc()).limit(limit).all()
        return [self._to_response(v) for v in visits]

    def create(self, db: Session, data: VisitCreate) -> VisitResponse:
        patient = db.query(PatientProfile).filter(PatientProfile.id == data.patient_profile_id).first()
        if not patient:
            raise CSMSException("Patient profile not found", status_code=404)

        today = datetime.utcnow().strftime("%Y%m%d")
        count = db.query(func.count(Visit.id)).filter(
            Visit.visit_number.like(f"{today}%")
        ).scalar() or 0
        visit_number = f"{today}{str(count + 1).zfill(4)}"
        data_dict = data.model_dump()
        visit = Visit(visit_number=visit_number, **data_dict)
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def update(self, db: Session, visit_id: str, data: VisitUpdate) -> VisitResponse:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(visit, field, value)
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def checkin(self, db: Session, visit_id: str) -> VisitResponse:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        visit.visit_status = VisitStatus.CHECKIN
        if visit.queue:
            visit.queue.status = QueueStatus.CALLING
            visit.queue.called_at = datetime.utcnow()
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def start_serving(self, db: Session, visit_id: str) -> VisitResponse:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        visit.visit_status = VisitStatus.SERVING
        if visit.queue:
            visit.queue.status = QueueStatus.SERVING
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def finish(self, db: Session, visit_id: str) -> VisitResponse:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        visit.visit_status = VisitStatus.FINISHED
        if visit.queue:
            visit.queue.status = QueueStatus.FINISHED
            visit.queue.finished_at = datetime.utcnow()
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def cancel(self, db: Session, visit_id: str) -> VisitResponse:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        visit.visit_status = VisitStatus.CANCELLED
        if visit.queue:
            visit.queue.status = QueueStatus.CANCELLED
            visit.queue.finished_at = datetime.utcnow()
        db.commit()
        db.refresh(visit)
        return self.get_by_id(db, visit.id)

    def _get_visit_with_relations(self, db: Session, visit_id: str) -> Visit:
        visit = db.query(Visit).options(
            joinedload(Visit.patient_profile).joinedload(PatientProfile.employee),
            joinedload(Visit.healthcare_professional).joinedload(HealthcareProfessional.employee),
            joinedload(Visit.queue),
            joinedload(Visit.medical_record),
            joinedload(Visit.soap_note),
            joinedload(Visit.vital_sign),
            joinedload(Visit.diagnoses),
            joinedload(Visit.visit_procedures),
            joinedload(Visit.prescription),
            joinedload(Visit.certificates),
            joinedload(Visit.attachments),
        ).filter(Visit.id == visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)
        return visit

    def _to_response(self, visit: Visit) -> VisitResponse:
        return VisitResponse(
            id=visit.id,
            patient_profile_id=visit.patient_profile_id,
            queue_id=visit.queue_id,
            healthcare_professional_id=visit.healthcare_professional_id,
            visit_type=visit.visit_type,
            visit_number=visit.visit_number,
            visit_date=visit.visit_date,
            complaint=visit.complaint,
            visit_status=visit.visit_status,
            created_at=visit.created_at,
            updated_at=visit.updated_at,
            patient_name=visit.patient_profile.employee.full_name if visit.patient_profile and visit.patient_profile.employee else None,
            doctor_name=visit.healthcare_professional.employee.full_name if visit.healthcare_professional and visit.healthcare_professional.employee else None,
            queue_number=visit.queue.queue_number if visit.queue else None,
        )


visit_service = VisitService()
