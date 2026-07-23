from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.hrd_ga.clinic.schemas import ClinicActivityLogCreate
from app.modules.hrd_ga.clinic.services import clinic_activity_log_service

router = APIRouter()


@router.get("/activity-logs", tags=["clinic-audit"])
def list_activity_logs(
    module: str | None = Query(None),
    user_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = clinic_activity_log_service.get_all(
        db, module=module, user_id=user_id, skip=(page - 1) * size, limit=size
    )
    return create_success_response(data=[item.model_dump() for item in items])

@router.post("/activity-logs", tags=["clinic-audit"])
def create_activity_log(
    body: ClinicActivityLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.user_id is None:
        body.user_id = current_user.id
    data = clinic_activity_log_service.log(db, body)
    return create_success_response(data=data.model_dump(), message="Activity logged")
