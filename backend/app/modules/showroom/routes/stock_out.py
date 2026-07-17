from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequirePermission
from app.models.user import User
from app.modules.showroom.schemas import StockOutCreate, StockOutUpdate
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/stock-out/stats",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def get_stock_out_stats(db: Session = Depends(get_db)):
    data = showroom_service.get_stock_out_stats(db)
    return create_success_response(data=data.model_dump())


@router.get(
    "/stock-out",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def list_stock_out(db: Session = Depends(get_db)):
    data = showroom_service.get_stock_out(db)
    return create_success_response(data=[row.model_dump() for row in data])


@router.post(
    "/stock-out",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_CREATE))],
)
def create_stock_out(
    body: StockOutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = showroom_service.create_stock_out(db, current_user.id, body)
    return create_success_response(
        data=data.model_dump(),
        message="Stock out created successfully",
    )


@router.put(
    "/stock-out/{stock_out_id}",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_UPDATE))],
)
def update_stock_out(
    stock_out_id: str,
    body: StockOutUpdate,
    db: Session = Depends(get_db),
):
    data = showroom_service.update_stock_out(db, stock_out_id, body)
    return create_success_response(
        data=data.model_dump(),
        message="Stock out updated successfully",
    )
