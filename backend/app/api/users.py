from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.session import get_db

from app.schemas.user import (
    UserResponse,
    UserCreate,
    UserUpdate,
    ProfileUpdate,
)

from app.schemas.role import RoleResponse
from app.common.responses import (
    SuccessResponse,
    create_success_response,
)

from app.common.pagination import (
    PaginationParams,
    PaginatedResponse,
    create_paginated_response,
)

from app.services.user_service import user_service

from app.dependencies.auth import get_current_user, get_current_token_payload
from app.dependencies.permission import RequirePermission

from app.constants.permissions import Permission

from app.repositories.user_repository import user_repo
from app.repositories.role_repository import role_repo

from app.core.exceptions import CSMSException

router = APIRouter()

# =============================================================================
# PROFILE
# =============================================================================


@router.get("/profile", response_model=SuccessResponse[UserResponse])
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = user_repo.get_by_id_with_roles(db, current_user.id)

    if not user:
        raise CSMSException("User not found", status_code=404)

    return create_success_response(
        data=user,
        message="Profile fetched successfully",
    )


@router.put("/profile", response_model=SuccessResponse[UserResponse])
def update_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_user = user_service.update_profile(
        db,
        user_id=current_user.id,
        profile_in=profile_in,
    )

    return create_success_response(
        data=updated_user,
        message="Profile updated successfully",
    )


# =============================================================================
# ROLE
# =============================================================================


@router.get(
    "/roles",
    response_model=SuccessResponse[list[RoleResponse]],
    dependencies=[
        Depends(RequirePermission(Permission.ROLE_VIEW)),
    ],
)
def list_roles(
    db: Session = Depends(get_db),
):
    roles = role_repo.get_all_with_permissions(db)

    return create_success_response(
        data=roles,
        message="Roles fetched successfully",
    )


# =============================================================================
# USERS
# =============================================================================


@router.get(
    "/",
    response_model=PaginatedResponse[UserResponse],
    dependencies=[
        Depends(RequirePermission(Permission.USER_VIEW)),
    ],
)
def list_users(
    params: PaginationParams = Depends(),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    users, total = user_service.get_users(
        db=db,
        skip=params.skip,
        limit=params.size,
        search=search,
    )

    return create_paginated_response(
        data=users,
        total=total,
        page=params.page,
        size=params.size,
    )


@router.post(
    "/",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(RequirePermission(Permission.USER_CREATE)),
    ],
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    user = user_service.create_user(
        db,
        user_in,
    )

    return create_success_response(
        data=user,
        message="User created successfully",
    )


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    dependencies=[
        Depends(RequirePermission(Permission.USER_VIEW)),
    ],
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = user_service.get_user(
        db,
        user_id,
    )

    return create_success_response(
        data=user,
        message="User fetched successfully",
    )


@router.put(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    dependencies=[
        Depends(RequirePermission(Permission.USER_UPDATE)),
    ],
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    user = user_service.update_user(
        db,
        user_id,
        user_in,
    )

    return create_success_response(
        data=user,
        message="User updated successfully",
    )


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[dict],
    dependencies=[
        Depends(RequirePermission(Permission.USER_DELETE)),
    ],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user_service.delete_user(
        db,
        user_id,
    )

    return create_success_response(
        data=None,
        message="User deleted successfully",
    )
