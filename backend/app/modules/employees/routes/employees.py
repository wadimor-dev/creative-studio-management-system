from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import create_success_response
from app.common.pagination import create_paginated_response
from app.constants.permissions import Permission
from app.core.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequirePermission
from app.models.user import User
from app.modules.employees.schemas import EmployeeCreate, EmployeeUpdate
from app.modules.employees.service import employee_service
from app.core.organization.employee.number_generator import employee_number_service

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_VIEW))],
)
def list_employees(
    branch_id: int | None = Query(None),
    department_id: int | None = Query(None),
    position_id: int | None = Query(None),
    division_id: int | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if search:
        items = employee_service.search(db, search, limit=size)
        return create_success_response(data=[item.model_dump() for item in items])

    items, total = employee_service.get_all(
        db,
        branch_id=branch_id,
        department_id=department_id,
        position_id=position_id,
        division_id=division_id,
        skip=(page - 1) * size,
        limit=size,
    )
    return create_paginated_response(
        data=[item.model_dump() for item in items],
        total=total,
        page=page,
        size=size,
    )


@router.get(
    "/number/generate",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_CREATE))],
)
def generate_employee_number(
    branch_code: str | None = Query(None),
    year: int | None = Query(None),
    db: Session = Depends(get_db),
):
    number = employee_number_service.generate(db, branch_code=branch_code, year=year)
    return create_success_response(data={"employee_number": number})


@router.get(
    "/me",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_VIEW))],
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = employee_service.get_by_user_id(db, current_user.id)
    if not data:
        return create_success_response(data=None, message="No employee profile found")
    return create_success_response(data=data.model_dump())


@router.get(
    "/{employee_id}",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_VIEW))],
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    data = employee_service.get_by_id(db, employee_id)
    return create_success_response(data=data.model_dump())


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_CREATE))],
)
def create_employee(
    body: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = employee_service.create(db, body)
    return create_success_response(
        data=data.model_dump(),
        message="Employee created successfully",
    )


@router.put(
    "/{employee_id}",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_UPDATE))],
)
def update_employee(
    employee_id: int,
    body: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    data = employee_service.update(db, employee_id, body)
    return create_success_response(
        data=data.model_dump(),
        message="Employee updated successfully",
    )


@router.delete(
    "/{employee_id}",
    dependencies=[Depends(RequirePermission(Permission.EMPLOYEE_DELETE))],
)
def delete_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    hard: bool = Query(False, description="Hard delete (permanent) if true"),
):
    if hard:
        employee_service.delete(db, employee_id)
        return create_success_response(message="Employee permanently deleted")
    employee_service.soft_delete(db, employee_id, current_user.id)
    return create_success_response(message="Employee soft-deleted successfully")
