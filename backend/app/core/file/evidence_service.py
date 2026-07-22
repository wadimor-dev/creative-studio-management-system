from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.core.file.models import WorkEvidence
from app.constants.work_activity import WorkEvidenceType, WorkActivityStatus
from app.schemas.work_evidence import WorkEvidenceCreate
from app.core.file.evidence_repository import work_evidence_repository
from app.repositories.work_activity_repository import work_activity_repository
from app.core.exceptions import CSMSException
from app.core.file.utils import validate_evidence_file, save_evidence_file


class WorkEvidenceService:

    def validate_before(self, db: Session, activity_id: int) -> None:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
        if activity.status != WorkActivityStatus.READY:
            raise CSMSException(f"Cannot start activity because status is {activity.status.value}", status_code=400)
        count = work_evidence_repository.count_by_type(db, activity_id, WorkEvidenceType.BEFORE)
        if count == 0:
            raise CSMSException("Cannot start activity: BEFORE evidence is required", status_code=400)

    def validate_after(self, db: Session, activity_id: int) -> None:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
        if activity.status != WorkActivityStatus.WORKING:
            raise CSMSException(f"Cannot finish activity because status is {activity.status.value}", status_code=400)
        count = work_evidence_repository.count_by_type(db, activity_id, WorkEvidenceType.AFTER)
        if count == 0:
            raise CSMSException("Cannot finish activity: AFTER evidence is required", status_code=400)

    def upload_evidence(self, db: Session, activity_id: int, user_id: int, type: WorkEvidenceType,
                        file: UploadFile, description: Optional[str] = None) -> WorkEvidence:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)

        if activity.user_id != user_id:
            raise CSMSException("You are not authorized to upload evidence for this activity", status_code=403)

        if type == WorkEvidenceType.BEFORE:
            if activity.status != WorkActivityStatus.READY:
                raise CSMSException(f"Cannot upload BEFORE evidence when status is {activity.status.value}", status_code=400)
            count = work_evidence_repository.count_by_type(db, activity_id, WorkEvidenceType.BEFORE)
            if count >= 1:
                raise CSMSException("Maximum 1 BEFORE evidence allowed", status_code=400)

        elif type == WorkEvidenceType.AFTER:
            if activity.status != WorkActivityStatus.WORKING:
                raise CSMSException(f"Cannot upload AFTER evidence when status is {activity.status.value}", status_code=400)
            count = work_evidence_repository.count_by_type(db, activity_id, WorkEvidenceType.AFTER)
            if count >= 1:
                raise CSMSException("Maximum 1 AFTER evidence allowed", status_code=400)

        elif type == WorkEvidenceType.PROGRESS:
            if activity.status != WorkActivityStatus.WORKING:
                raise CSMSException(f"Cannot upload PROGRESS evidence when status is {activity.status.value}", status_code=400)

        file_size = validate_evidence_file(file)

        file_prefix = type.value.lower()
        file_path = save_evidence_file(file, activity_id, file_prefix)

        obj_in = WorkEvidenceCreate(type=type, description=description)
        evidence = work_evidence_repository.create(
            db=db, obj_in=obj_in, work_activity_id=activity_id,
            file_path=file_path, file_name=file.filename,
            file_size=file_size, mime_type=file.content_type, user_id=user_id,
        )

        db.commit()
        db.refresh(evidence)
        return evidence

    def get_activity_evidence(self, db: Session, activity_id: int) -> List[WorkEvidence]:
        activity = work_activity_repository.find_by_id(db, activity_id)
        if not activity:
            raise CSMSException("Activity not found", status_code=404)
        return work_evidence_repository.find_by_activity(db, activity_id)

    def delete_evidence(self, db: Session, id: int, user_id: int) -> bool:
        pass


work_evidence_service = WorkEvidenceService()
