from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.showroom_v2.schemas import (
    OpnameSessionCreate, OpnameItemCreate, RestockRequestCreate, MaintenanceCreate, ReservationCreate, SuccessResponse,
)
from app.modules.showroom_v2.services.stock_control_service import StockControlService

router = APIRouter()


@router.get("/opname")
def get_opname_sessions(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sessions = StockControlService.get_opname_sessions(db, status)
    return SuccessResponse(data=sessions)


@router.post("/opname")
def create_opname_session(
    data: OpnameSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.create_opname_session(db, data, current_user.id)
    return SuccessResponse(data=result, message="Opname session created")


@router.post("/opname/{session_id}/items")
def add_opname_item(
    session_id: int,
    data: OpnameItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.add_opname_item(db, session_id, data)
    return SuccessResponse(data=result, message="Opname item added")


@router.post("/opname/{session_id}/complete")
def complete_opname(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.complete_opname(db, session_id, current_user.id)
    return SuccessResponse(data=result, message="Opname completed")


@router.post("/opname/{session_id}/approve")
def approve_opname(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.approve_opname(db, session_id, current_user.id)
    return SuccessResponse(data=result, message="Opname approved")


@router.get("/restock")
def get_restock_requests(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requests = StockControlService.get_restock_requests(db, status)
    return SuccessResponse(data=requests)


@router.post("/restock")
def create_restock_request(
    data: RestockRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.create_restock_request(db, data, current_user.id)
    return SuccessResponse(data=result, message="Restock request created")


@router.post("/restock/{request_id}/approve")
def approve_restock(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.approve_restock(db, request_id, current_user.id)
    return SuccessResponse(data=result, message="Restock approved")


@router.get("/maintenance")
def get_maintenance(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = StockControlService.get_maintenance(db, status)
    return SuccessResponse(data=records)


@router.post("/maintenance")
def create_maintenance(
    data: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.create_maintenance(db, data, current_user.id)
    return SuccessResponse(data=result, message="Maintenance created")


@router.post("/maintenance/{maintenance_id}/complete")
def complete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.complete_maintenance(db, maintenance_id, current_user.id)
    return SuccessResponse(data=result, message="Maintenance completed")


@router.get("/reservations")
def get_reservations(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = StockControlService.get_reservations(db, status)
    return SuccessResponse(data=records)


@router.post("/reservations")
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = StockControlService.create_reservation(db, data, current_user.id)
    return SuccessResponse(data=result, message="Reservation created")
