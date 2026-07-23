from datetime import date, datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.modules.hrd_ga.clinic.schemas import (
    QueueCreate, QueueUpdate, QueueStatus,
    VisitCreate, VisitUpdate, VisitStatus,
)
from app.modules.hrd_ga.clinic.services import queue_service, visit_service

router = APIRouter()


# ──────── QUEUES ────────

@router.get("/queues", tags=["clinic-queues"])
def list_queues(
    queue_date: date | None = Query(None),
    status: QueueStatus | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = queue_service.get_all(db, queue_date=queue_date, status=status, skip=(page - 1) * size, limit=size)
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/queues/current", tags=["clinic-queues"])
def get_current_queue(db: Session = Depends(get_db)):
    data = queue_service.get_current_queue(db)
    return create_success_response(data=data.model_dump() if data else None)

@router.get("/queues/waiting-count", tags=["clinic-queues"])
def get_waiting_count(db: Session = Depends(get_db)):
    count = queue_service.get_waiting_count(db)
    return create_success_response(data={"waiting_count": count})

@router.get("/queues/{queue_id}", tags=["clinic-queues"])
def get_queue(queue_id: str, db: Session = Depends(get_db)):
    data = queue_service.get_by_id(db, queue_id)
    return create_success_response(data=data.model_dump())

@router.post("/queues", status_code=status.HTTP_201_CREATED, tags=["clinic-queues"])
def create_queue(body: QueueCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = queue_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Queue created successfully")

@router.put("/queues/{queue_id}/status", tags=["clinic-queues"])
def update_queue_status(queue_id: str, body: QueueUpdate, db: Session = Depends(get_db)):
    new_status = body.status
    if new_status is None:
        return create_success_response(message="No status provided")
    data = queue_service.update_status(db, queue_id, new_status)
    return create_success_response(data=data.model_dump(), message=f"Queue status updated to {new_status.value}")


# ──────── VISITS ────────

@router.get("/visits", tags=["clinic-visits"])
def list_visits(
    patient_profile_id: str | None = Query(None, alias="patient_id"),
    status: VisitStatus | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = visit_service.get_all(
        db, patient_profile_id=patient_profile_id, status=status,
        visit_date_from=date_from, visit_date_to=date_to,
        skip=(page - 1) * size, limit=size,
    )
    return create_success_response(data=[item.model_dump() for item in items])

@router.get("/visits/{visit_id}", tags=["clinic-visits"])
def get_visit(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.get_by_id(db, visit_id)
    return create_success_response(data=data.model_dump())

@router.get("/visits/{visit_id}/detail", tags=["clinic-visits"])
def get_visit_detail(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.get_detail(db, visit_id)
    return create_success_response(data=data.model_dump())

@router.post("/visits", status_code=status.HTTP_201_CREATED, tags=["clinic-visits"])
def create_visit(body: VisitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = visit_service.create(db, body)
    return create_success_response(data=data.model_dump(), message="Visit created successfully")

@router.put("/visits/{visit_id}", tags=["clinic-visits"])
def update_visit(visit_id: str, body: VisitUpdate, db: Session = Depends(get_db)):
    data = visit_service.update(db, visit_id, body)
    return create_success_response(data=data.model_dump(), message="Visit updated successfully")

@router.put("/visits/{visit_id}/checkin", tags=["clinic-visits"])
def checkin_visit(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.checkin(db, visit_id)
    return create_success_response(data=data.model_dump(), message="Visit checked in")

@router.put("/visits/{visit_id}/start-serving", tags=["clinic-visits"])
def start_serving(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.start_serving(db, visit_id)
    return create_success_response(data=data.model_dump(), message="Service started")

@router.put("/visits/{visit_id}/finish", tags=["clinic-visits"])
def finish_visit(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.finish(db, visit_id)
    return create_success_response(data=data.model_dump(), message="Visit finished")

@router.put("/visits/{visit_id}/cancel", tags=["clinic-visits"])
def cancel_visit(visit_id: str, db: Session = Depends(get_db)):
    data = visit_service.cancel(db, visit_id)
    return create_success_response(data=data.model_dump(), message="Visit cancelled")
