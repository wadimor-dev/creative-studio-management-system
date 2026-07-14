from typing import List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from app.models.work_activity import WorkActivity
from app.constants.work_activity import WorkActivityStatus
from app.schemas.work_activity import WorkActivityCreate, WorkActivityUpdate

class WorkActivityRepository:
    
    def create(self, db: Session, obj_in: WorkActivityCreate, user_id: int) -> WorkActivity:
        db_obj = WorkActivity(
            user_id=user_id,
            category_id=obj_in.category_id,
            activity_name=obj_in.activity_name,
            notes=obj_in.notes,
            created_by=user_id,
            updated_by=user_id
        )
        db.add(db_obj)
        db.flush()
        return db_obj
        
    def find_by_id(self, db: Session, id: int) -> Optional[WorkActivity]:
        return db.query(WorkActivity).filter(
            WorkActivity.id == id,
            WorkActivity.is_deleted == False
        ).first()
        
    def find_today(self, db: Session) -> List[WorkActivity]:
        today_start = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0)
        return db.query(WorkActivity).filter(
            WorkActivity.created_at >= today_start,
            WorkActivity.is_deleted == False
        ).order_by(desc(WorkActivity.created_at)).all()
        
    def find_by_user(self, db: Session, user_id: int) -> List[WorkActivity]:
        return db.query(WorkActivity).filter(
            WorkActivity.user_id == user_id,
            WorkActivity.is_deleted == False
        ).order_by(desc(WorkActivity.created_at)).all()
        
    def find_active_by_user(self, db: Session, user_id: int) -> Optional[WorkActivity]:
        return db.query(WorkActivity).filter(
            WorkActivity.user_id == user_id,
            WorkActivity.is_deleted == False,
            WorkActivity.status.in_([WorkActivityStatus.WORKING, WorkActivityStatus.PAUSED])
        ).first()
        
    def update(self, db: Session, db_obj: WorkActivity, obj_in: dict, user_id: int, commit: bool = True) -> WorkActivity:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db_obj.updated_by = user_id
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        else:
            db.flush()
        return db_obj
        
    def soft_delete(self, db: Session, id: int, user_id: int) -> bool:
        db_obj = self.find_by_id(db, id)
        if not db_obj:
            return False
        db_obj.is_deleted = True
        db_obj.deleted_at = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        db_obj.updated_by = user_id
        db.add(db_obj)
        db.flush()
        return True

work_activity_repository = WorkActivityRepository()
