from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.permission import RequirePermission
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/locations",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def list_locations(db: Session = Depends(get_db)):
    data = showroom_service.get_locations(db)
    return create_success_response(data=[loc.model_dump() for loc in data])
