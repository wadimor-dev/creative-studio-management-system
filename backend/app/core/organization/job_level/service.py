from typing import Optional
from sqlalchemy.orm import Session
from app.core.organization.job_level.models import JobLevel
from app.core.organization.job_level.schemas import JobLevelCreate, JobLevelUpdate


class JobLevelService:
    def get_all(self, db: Session, is_active: Optional[bool] = None):
        q = db.query(JobLevel)
        if is_active is not None:
            q = q.filter(JobLevel.is_active == is_active)
        return q.order_by(JobLevel.level).all()

    def get_by_id(self, db: Session, job_level_id: int) -> Optional[JobLevel]:
        return db.query(JobLevel).filter(JobLevel.id == job_level_id).first()

    def create(self, db: Session, data: JobLevelCreate) -> JobLevel:
        obj = JobLevel(**data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, job_level_id: int, data: JobLevelUpdate) -> Optional[JobLevel]:
        obj = self.get_by_id(db, job_level_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, job_level_id: int) -> bool:
        obj = self.get_by_id(db, job_level_id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True


job_level_service = JobLevelService()
