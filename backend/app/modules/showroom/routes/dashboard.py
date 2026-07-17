from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.permission import RequirePermission
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/dashboard",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def get_dashboard(db: Session = Depends(get_db)):
    data = showroom_service.get_dashboard_stats(db)
    return create_success_response(data=data.model_dump())


@router.get(
    "/movements",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def get_movements(
    limit: int | None = Query(None, ge=1, le=100),
    location: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Shared movements endpoint.
    - Dashboard: ?limit=5 → flat product string summary
    - Stock page: no limit / with location → rich product {sku, name}
    """
    if limit is not None and limit <= 5 and location is None:
        data = showroom_service.get_recent_movements(db, limit=limit)
        return create_success_response(data=[m.model_dump() for m in data])

    data = showroom_service.get_stock_movements(db, location=location)
    if limit is not None:
        data = data[:limit]
    return create_success_response(data=[m.model_dump() for m in data])
