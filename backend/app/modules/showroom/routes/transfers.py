from fastapi import APIRouter, Depends, Query
from fastapi import status as http_status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequirePermission
from app.models.user import User
from app.modules.showroom.schemas import TransferCreate, TransferUpdate
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/transfers/stats",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def get_transfer_stats(db: Session = Depends(get_db)):
    data = showroom_service.get_transfer_stats(db)
    return create_success_response(data=data.model_dump())


@router.get(
    "/transfers",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def list_transfers(
    status_filter: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    data = showroom_service.get_transfers(db, status=status_filter)
    return create_success_response(data=[t.model_dump() for t in data])


@router.post(
    "/transfers",
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_CREATE))],
)
def create_transfer(
    body: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = showroom_service.create_transfer(db, current_user.id, body)
    return create_success_response(
        data=data.model_dump(),
        message="Transfer created successfully",
    )


@router.put(
    "/transfers/{transfer_id}",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_UPDATE))],
)
def update_transfer(
    transfer_id: str,
    body: TransferUpdate,
    db: Session = Depends(get_db),
):
    data = showroom_service.update_transfer(db, transfer_id, body)
    return create_success_response(
        data=data.model_dump(),
        message="Transfer updated successfully",
    )


@router.post(
    "/transfers/{transfer_id}/cancel",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_UPDATE))],
)
def cancel_transfer(
    transfer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = showroom_service.cancel_transfer(db, current_user.id, transfer_id)
    return create_success_response(
        data=data.model_dump(),
        message="Transfer cancelled successfully",
    )


@router.post(
    "/transfers/{transfer_id}/confirm",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_UPDATE))],
)
def confirm_transfer(
    transfer_id: str,
    db: Session = Depends(get_db),
):
    data = showroom_service.confirm_transfer(db, transfer_id)
    return create_success_response(
        data=data.model_dump(),
        message="Transfer confirmed successfully",
    )
