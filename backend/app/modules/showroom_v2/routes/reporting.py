from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.modules.showroom_v2.schemas import SuccessResponse
from app.modules.showroom_v2.services.reporting_service import ReportingService

router = APIRouter()


@router.get("/kpi")
def get_kpi(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    kpi = ReportingService.get_kpi(db)
    return SuccessResponse(data=kpi)


@router.get("/movement-summary")
def get_movement_summary(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = ReportingService.get_movement_summary(db, days)
    return SuccessResponse(data=summary)


@router.get("/stock-by-location")
def get_stock_by_location(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = ReportingService.get_stock_by_location(db)
    return SuccessResponse(data=data)


@router.get("/product-history/{product_id}")
def get_product_history(
    product_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = ReportingService.get_product_movement_history(db, product_id, limit)
    return SuccessResponse(data=history)


@router.get("/borrowing-summary")
def get_borrowing_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = ReportingService.get_borrowing_summary(db)
    return SuccessResponse(data=summary)


@router.get("/guest-summary")
def get_guest_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = ReportingService.get_guest_summary(db)
    return SuccessResponse(data=summary)
