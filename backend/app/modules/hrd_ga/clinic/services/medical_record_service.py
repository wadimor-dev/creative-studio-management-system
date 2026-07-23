from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.core.exceptions import CSMSException
from app.modules.hrd_ga.clinic.models.medical_record import MedicalRecord, MedicalRecordStatus
from app.modules.hrd_ga.clinic.models.visit import Visit
from app.modules.hrd_ga.clinic.schemas import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse


class MedicalRecordService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[MedicalRecordResponse]:
        items = db.query(MedicalRecord).options(
            joinedload(MedicalRecord.visit)
        ).order_by(MedicalRecord.record_number.desc()).offset(skip).limit(limit).all()
        return [MedicalRecordResponse.model_validate(mr) for mr in items]

    def get_by_id(self, db: Session, record_id: str) -> MedicalRecordResponse:
        mr = db.query(MedicalRecord).options(
            joinedload(MedicalRecord.visit)
        ).filter(MedicalRecord.id == record_id).first()
        if not mr:
            raise CSMSException("Medical record not found", status_code=404)
        return MedicalRecordResponse.model_validate(mr)

    def get_by_visit_id(self, db: Session, visit_id: str) -> Optional[MedicalRecordResponse]:
        mr = db.query(MedicalRecord).filter(MedicalRecord.visit_id == visit_id).first()
        if not mr:
            return None
        return MedicalRecordResponse.model_validate(mr)

    def create(self, db: Session, data: MedicalRecordCreate) -> MedicalRecordResponse:
        visit = db.query(Visit).filter(Visit.id == data.visit_id).first()
        if not visit:
            raise CSMSException("Visit not found", status_code=404)

        today = __import__("datetime").datetime.utcnow().strftime("%Y%m%d")
        count = db.query(func.count(MedicalRecord.id)).filter(
            MedicalRecord.record_number.like(f"MR-{today}%")
        ).scalar() or 0
        record_number = f"MR-{today}{str(count + 1).zfill(4)}"

        mr = MedicalRecord(record_number=record_number, **data.model_dump(exclude={"record_number"}))
        db.add(mr)
        db.commit()
        db.refresh(mr)
        return MedicalRecordResponse.model_validate(mr)

    def update(self, db: Session, record_id: str, data: MedicalRecordUpdate) -> MedicalRecordResponse:
        mr = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
        if not mr:
            raise CSMSException("Medical record not found", status_code=404)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(mr, field, value)
        db.commit()
        db.refresh(mr)
        return MedicalRecordResponse.model_validate(mr)

    def finalize(self, db: Session, record_id: str) -> MedicalRecordResponse:
        return self.update(db, record_id, MedicalRecordUpdate(status=MedicalRecordStatus.FINAL))


medical_record_service = MedicalRecordService()
