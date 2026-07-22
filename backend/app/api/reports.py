from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database.session import get_db

from app.common.responses import (
    SuccessResponse,
    create_success_response,
)

from app.services.report_engine import report_engine

from app.dependencies.permission import RequirePermission
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.constants.permissions import Permission
from app.constants.role import RoleType

router = APIRouter()


@router.get(
    "",
    response_model=SuccessResponse[Any],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.REPORT_VIEW
            )
        )
    ],
)
def get_reports(
    type: str = Query(
        "daily",
        description="Report type (daily, weekly, monthly)",
    ),
    date: Optional[str] = Query(
        None,
        description="Date for daily report (YYYY-MM-DD)",
    ),
    month: Optional[int] = Query(
        None,
        description="Month for monthly report",
    ),
    year: Optional[int] = Query(
        None,
        description="Year for monthly report",
    ),
    user_id: Optional[int] = Query(
        None,
        description="Filter by User",
    ),
    category_id: Optional[int] = Query(
        None,
        description="Filter by Category",
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by Status",
    ),
    division: Optional[str] = Query(
        None,
        description="Filter by Division",
    ),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * size

    filters = {}

    if date:
        filters["date"] = date

    if month:
        filters["month"] = month

    if year:
        filters["year"] = year

    if category_id:
        filters["category_id"] = category_id

    if status:
        filters["status"] = status

    if division:
        filters["division"] = division

    # STAFF hanya melihat report miliknya sendiri
    if not any(r.name == RoleType.ADMIN for r in current_user.roles):
        filters["user_id"] = current_user.id
    elif user_id:
        filters["user_id"] = user_id

    data = report_engine.get_report_data(
        db=db,
        report_type=type,
        skip=skip,
        limit=size,
        **filters,
    )

    return create_success_response(
        data=data,
        message="Reports fetched successfully",
    )