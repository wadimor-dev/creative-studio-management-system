from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.hrd_ga.creative.showroom.schemas import SuccessResponse
from app.modules.hrd_ga.creative.showroom.services.dashboard_service import DashboardService
from app.modules.hrd_ga.creative.showroom.services.analytics_service import AnalyticsService
from app.core.storage.snapshot_service import SnapshotService
from app.modules.hrd_ga.creative.showroom.services.borrowing_service import BorrowingService
from app.modules.hrd_ga.creative.showroom.services.guest_service import GuestService

router = APIRouter()


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=DashboardService.get_summary(db))


@router.get("/borrowing-stats")
def get_borrowing_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=BorrowingService.get_stats(db))


@router.get("/guest-stats")
def get_guest_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=GuestService.get_stats(db))


@router.get("/overdue-borrowings")
def get_overdue_borrowings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=BorrowingService.get_overdue(db))


@router.get("/movements")
def get_recent_movements(
    limit: int = Query(20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=DashboardService.get_recent_movements(db, limit=limit))


@router.get("/heatmap")
def get_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=DashboardService.get_heatmap_data(db))


@router.get("/analytics/trends")
def get_trends(
    days: int = Query(30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=AnalyticsService.get_movement_trends(db, days=days))


@router.get("/analytics/top-products")
def get_top_products(
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=AnalyticsService.get_top_products(db, limit=limit))


@router.get("/analytics/borrowing")
def get_borrowing_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=AnalyticsService.get_borrowing_analytics(db))


@router.post("/snapshot")
def create_snapshot(
    snapshot_type: str = Query("MANUAL"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=SnapshotService.create_snapshot(db, snapshot_type=snapshot_type), message="Snapshot created")


@router.post("/rebuild-summary")
def rebuild_summary(
    target_date: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=SnapshotService.rebuild_daily_summary(db, target_date=target_date), message="Summary rebuilt")


@router.get("/summary-history")
def get_summary_history(
    days: int = Query(30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SuccessResponse(data=SnapshotService.get_summary_history(db, days=days))
