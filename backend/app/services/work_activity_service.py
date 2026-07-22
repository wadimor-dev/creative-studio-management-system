from typing import List
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.work_activity import WorkActivity
from app.constants.work_activity import WorkActivityStatus
from app.schemas.work_activity import WorkActivityCreate, WorkActivityUpdate, WorkAssetPayload
from app.repositories.work_activity_repository import work_activity_repository
from app.core.exceptions import CSMSException
from app.services.work_asset_service import work_asset_service
from app.core.file.evidence_service import work_evidence_service
from app.utils.generator import generate_work_reference


class WorkActivityService:

    def create_activity(self, db: Session, obj_in: WorkActivityCreate, user_id: int) -> WorkActivity:
        activity = work_activity_repository.create(db, obj_in, user_id)
        db.commit()
        db.refresh(activity)
        return activity
        
    def start_activity(self, db: Session, activity_id: int, user_id: int, assets: List[WorkAssetPayload] = None) -> WorkActivity:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
            
        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to start this activity", status_code=403)
            
        if activity.status != WorkActivityStatus.READY:
            raise CSMSException(f"Cannot start activity because its status is {activity.status.value}", status_code=400)
            
        active_task = work_activity_repository.find_active_by_user(db, user_id)
        if active_task:
            raise CSMSException(f"You cannot start a new activity because you have an active activity: '{active_task.activity_name}'", status_code=400)

        work_evidence_service.validate_before(db, activity_id)

        if assets:
            if len({a.item_id for a in assets}) != len(assets):
                raise CSMSException("Duplicate items in assets payload not allowed", status_code=400)

            ref_number = generate_work_reference(activity_id)
            work_asset_service.borrow_assets(db, activity_id, user_id, assets, reference=ref_number)

        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        updates = {
            "status": WorkActivityStatus.WORKING,
            "start_time": now,
            "worked_seconds": 0,
            "current_session_started_at": now
        }
        activity = work_activity_repository.update(db, activity, updates, user_id, commit=False)
        db.commit()
        db.refresh(activity)
        return activity

    def finish_activity(self, db: Session, activity_id: int, user_id: int) -> WorkActivity:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
            
        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to finish this activity", status_code=403)
            
        if activity.status != WorkActivityStatus.WORKING:
            raise CSMSException(f"Cannot finish activity because its status is {activity.status.value}", status_code=400)

        work_evidence_service.validate_after(db, activity_id)

        return_reference = f"{generate_work_reference(activity_id)}-RETURN"
        work_asset_service.return_assets(db, activity_id, user_id, reference=return_reference)

        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        worked_seconds = activity.worked_seconds
        if activity.current_session_started_at:
            worked_seconds += int((now - activity.current_session_started_at).total_seconds())

        updates = {
            "status": WorkActivityStatus.COMPLETED,
            "end_time": now,
            "worked_seconds": worked_seconds,
            "current_session_started_at": None
        }
        activity = work_activity_repository.update(db, activity, updates, user_id, commit=False)
        db.commit()
        db.refresh(activity)
        return activity

    def pause_activity(self, db: Session, activity_id: int, user_id: int) -> WorkActivity:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
            
        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to pause this activity", status_code=403)
            
        if activity.status != WorkActivityStatus.WORKING:
            raise CSMSException(f"Cannot pause activity because its status is {activity.status.value}", status_code=400)
            
        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        worked_seconds = activity.worked_seconds
        if activity.current_session_started_at:
            worked_seconds += int((now - activity.current_session_started_at).total_seconds())
            
        updates = {
            "status": WorkActivityStatus.PAUSED,
            "worked_seconds": worked_seconds,
            "current_session_started_at": None
        }
        activity = work_activity_repository.update(db, activity, updates, user_id, commit=False)
        db.commit()
        db.refresh(activity)
        return activity

    def resume_activity(self, db: Session, activity_id: int, user_id: int) -> WorkActivity:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
            
        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to resume this activity", status_code=403)
            
        if activity.status != WorkActivityStatus.PAUSED:
            raise CSMSException(f"Cannot resume activity because its status is {activity.status.value}", status_code=400)
            
        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        updates = {
            "status": WorkActivityStatus.WORKING,
            "current_session_started_at": now
        }
        activity = work_activity_repository.update(db, activity, updates, user_id, commit=False)
        db.commit()
        db.refresh(activity)
        return activity

    def cancel_activity(self, db: Session, activity_id: int, user_id: int) -> WorkActivity:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
            
        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to cancel this activity", status_code=403)
            
        if activity.status in [WorkActivityStatus.COMPLETED, WorkActivityStatus.CANCELLED]:
            raise CSMSException(f"Cannot cancel activity because its status is {activity.status.value}", status_code=400)

        cancel_reference = f"{generate_work_reference(activity_id)}-CANCEL"
        work_asset_service.return_assets(db, activity_id, user_id, reference=cancel_reference)

        now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
        worked_seconds = activity.worked_seconds
        if activity.current_session_started_at:
            worked_seconds += int((now - activity.current_session_started_at).total_seconds())

        updates = {
            "status": WorkActivityStatus.CANCELLED,
            "end_time": now,
            "worked_seconds": worked_seconds,
            "current_session_started_at": None
        }
        activity = work_activity_repository.update(db, activity, updates, user_id, commit=False)
        db.commit()
        db.refresh(activity)
        return activity


work_activity_service = WorkActivityService()
