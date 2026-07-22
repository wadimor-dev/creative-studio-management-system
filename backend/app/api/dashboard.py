from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database.session import get_db

from app.services.dashboard_service import dashboard_service

from app.common.responses import (
    SuccessResponse,
    create_success_response,
)

from app.dependencies.permission import RequirePermission

from app.constants.permissions import Permission

router = APIRouter()


@router.get(
    "",
    response_model=SuccessResponse[Any],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.DASHBOARD_VIEW
            )
        )
    ],
)
def get_dashboard_data(
    days: int = Query(
        7,
        ge=1,
        le=365,
        description="Number of days for chart data",
    ),
    db: Session = Depends(get_db),
):
    metrics = dashboard_service.get_dashboard(
        db=db,
        days=days,
    )

    return create_success_response(
        data=metrics,
        message="Dashboard data fetched successfully",
    )