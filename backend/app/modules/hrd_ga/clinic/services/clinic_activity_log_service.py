from typing import Optional, List
from sqlalchemy.orm import Session
from app.modules.hrd_ga.clinic.models.clinic_activity_log import ClinicActivityLog
from app.modules.hrd_ga.clinic.schemas import ClinicActivityLogCreate, ClinicActivityLogResponse


class ClinicActivityLogService:

    def get_all(self, db: Session, skip: int = 0, limit: int = 100,
                module: Optional[str] = None,
                user_id: Optional[int] = None) -> List[ClinicActivityLogResponse]:
        query = db.query(ClinicActivityLog)
        if module:
            query = query.filter(ClinicActivityLog.module == module)
        if user_id is not None:
            query = query.filter(ClinicActivityLog.user_id == user_id)
        items = query.order_by(ClinicActivityLog.created_at.desc()).offset(skip).limit(limit).all()
        return [ClinicActivityLogResponse.model_validate(item) for item in items]

    def log(self, db: Session, data: ClinicActivityLogCreate) -> ClinicActivityLogResponse:
        entry = ClinicActivityLog(**data.model_dump())
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return ClinicActivityLogResponse.model_validate(entry)


clinic_activity_log_service = ClinicActivityLogService()
