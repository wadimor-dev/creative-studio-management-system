from fastapi import APIRouter, Depends, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.common.responses import SuccessResponse, create_success_response
from app.schemas.work_activity import WorkActivityCreate, WorkActivityResponse, WorkActivityStartRequest
from app.schemas.work_evidence import WorkEvidenceResponse
from app.services.work_activity_service import work_activity_service
from app.services.work_evidence_service import work_evidence_service
from app.repositories.work_activity_repository import work_activity_repository
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.constants.work_activity import WorkEvidenceType
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission

router = APIRouter()

@router.post("", response_model=SuccessResponse[WorkActivityResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequirePermission(Permission.WORK_CREATE))])
def create_work_activity(
    activity_in: WorkActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.create_activity(db, activity_in, current_user.id)
    return create_success_response(data=activity, message="Work activity created successfully")

@router.patch("/{id}/start", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_START))])
def start_work_activity(
    id: int,
    req: WorkActivityStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.start_activity(db, id, current_user.id, req.assets)
    return create_success_response(data=activity, message="Work activity started successfully")

@router.patch("/{id}/pause", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_PAUSE))])
def pause_work_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.pause_activity(db, id, current_user.id)
    return create_success_response(data=activity, message="Work activity paused successfully")

@router.patch("/{id}/resume", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_RESUME))])
def resume_work_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.resume_activity(db, id, current_user.id)
    return create_success_response(data=activity, message="Work activity resumed successfully")

@router.patch("/{id}/cancel", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_CANCEL))])
def cancel_work_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.cancel_activity(db, id, current_user.id)
    return create_success_response(data=activity, message="Work activity cancelled successfully")

@router.patch("/{id}/finish", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_FINISH))])
def finish_work_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_service.finish_activity(db, id, current_user.id)
    return create_success_response(data=activity, message="Work activity finished successfully")

@router.post("/{id}/evidence", response_model=SuccessResponse[WorkEvidenceResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequirePermission(Permission.WORK_EVIDENCE_UPLOAD))])
def upload_work_evidence(
    id: int,
    type: WorkEvidenceType = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    evidence = work_evidence_service.upload_evidence(
        db=db, 
        activity_id=id, 
        user_id=current_user.id, 
        type=type, 
        file=file, 
        description=description
    )
    return create_success_response(data=evidence, message="Evidence uploaded successfully")

@router.get("/{id}/evidences", response_model=SuccessResponse[List[WorkEvidenceResponse]], dependencies=[Depends(RequirePermission(Permission.WORK_EVIDENCE_VIEW))])
def get_work_evidences(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    evidences = work_evidence_service.get_activity_evidence(db, id)
    return create_success_response(data=evidences, message="Evidences fetched successfully")

@router.get("/me", response_model=SuccessResponse[List[WorkActivityResponse]], dependencies=[Depends(RequirePermission(Permission.WORK_VIEW))])
def get_my_work_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activities = work_activity_repository.find_by_user(db, current_user.id)
    return create_success_response(data=activities, message="Retrieved work activities successfully")

@router.get("/me/today", response_model=SuccessResponse[List[WorkActivityResponse]], dependencies=[Depends(RequirePermission(Permission.WORK_VIEW))])
def get_my_work_activities_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    activities = work_activity_repository.find_by_user(db, current_user.id)
    today_activities = [a for a in activities if a.created_at and a.created_at >= today_start]
    
    return create_success_response(data=today_activities, message="Retrieved today's work activities successfully")

@router.get("/current", response_model=SuccessResponse[Optional[WorkActivityResponse]], dependencies=[Depends(RequirePermission(Permission.WORK_VIEW))])
def get_current_work_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = work_activity_repository.find_active_by_user(db, current_user.id)
    return create_success_response(data=activity, message="Retrieved current work activity successfully")

@router.get("/{id}", response_model=SuccessResponse[WorkActivityResponse], dependencies=[Depends(RequirePermission(Permission.WORK_VIEW))])
def get_work_activity(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.exceptions.base import CSMSException
    activity = work_activity_repository.find_by_id(db, id)
    if not activity:
        raise CSMSException("Work activity not found", status_code=404)
    return create_success_response(data=activity, message="Retrieved work activity successfully")
