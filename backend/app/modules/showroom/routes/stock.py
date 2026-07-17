from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.permission import RequirePermission
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/stock",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def get_stock(
    location: str | None = Query(None),
    db: Session = Depends(get_db),
):
    data = showroom_service.get_stock_stats(db, location=location)
    return create_success_response(data=data.model_dump())
