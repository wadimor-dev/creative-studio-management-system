from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.constants.permissions import Permission
from app.database.session import get_db
from app.dependencies.permission import RequirePermission
from app.modules.showroom.services import showroom_service

router = APIRouter()


@router.get(
    "/products",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def list_products(
    search: str | None = Query(None),
    limit: int = Query(200, ge=1, le=500),
    db: Session = Depends(get_db),
):
    data = showroom_service.get_products(db, search=search, limit=limit)
    return create_success_response(data=[p.model_dump() for p in data])


@router.get(
    "/scanner/{code}",
    dependencies=[Depends(RequirePermission(Permission.SHOWROOM_VIEW))],
)
def resolve_scanner_code(code: str, db: Session = Depends(get_db)):
    data = showroom_service.resolve_scan(db, code)
    return create_success_response(
        data=data,
        message=f"Code resolved to a {data.get('type')}",
    )
