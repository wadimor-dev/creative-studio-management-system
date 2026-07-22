from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.showroom_v2.schemas import SuccessResponse
from app.modules.showroom_v2.services.reporting_service import ReportingService
from app.modules.showroom_v2.services.borrowing_service import BorrowingService
from app.modules.showroom_v2.services.guest_service import GuestService

router = APIRouter()


@router.get("/")
def get_dashboard_kpi(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    kpi = ReportingService.get_kpi(db)
    return SuccessResponse(data=kpi)


@router.get("/borrowing-stats")
def get_borrowing_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = BorrowingService.get_stats(db)
    return SuccessResponse(data=stats)


@router.get("/guest-stats")
def get_guest_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stats = GuestService.get_stats(db)
    return SuccessResponse(data=stats)


@router.get("/overdue-borrowings")
def get_overdue_borrowings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowings = BorrowingService.get_overdue(db)
    return SuccessResponse(data=borrowings)
