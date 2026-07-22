from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.showroom_v2.schemas import SuccessResponse
from app.modules.showroom_v2.services.borrowing_service import BorrowingService

router = APIRouter()


class ExtendBorrowing(BaseModel):
    expected_return_date: str


class CancelBorrowing(BaseModel):
    reason: Optional[str] = None


@router.get("/")
def get_borrowings(
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowings = BorrowingService.get_all(db, status)
    return SuccessResponse(data=borrowings)


@router.get("/overdue")
def get_overdue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowings = BorrowingService.get_overdue(db)
    return SuccessResponse(data=borrowings)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = BorrowingService.get_stats(db)
    return SuccessResponse(data=stats)


@router.get("/{borrowing_id}")
def get_borrowing(
    borrowing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowing = BorrowingService.get_by_id(db, borrowing_id)
    return SuccessResponse(data=borrowing)


@router.post("/{borrowing_id}/extend")
def extend_borrowing(
    borrowing_id: int,
    data: ExtendBorrowing,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = BorrowingService.extend_borrowing(db, borrowing_id, data.expected_return_date)
    return SuccessResponse(data=result, message="Borrowing extended")


@router.post("/{borrowing_id}/cancel")
def cancel_borrowing(
    borrowing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = BorrowingService.cancel_borrowing(db, borrowing_id, current_user.id)
    return SuccessResponse(data=result, message="Borrowing cancelled")
