from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database.session import get_db
from app.core.authorization.repositories import (
    permission_repo,
    role_permission_repo,
)
from app.core.authorization.schemas import PermissionResponse
from app.core.authorization.services import sync_permissions_from_enum
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate, RoleWithPermissions
from app.services.role_service import role_service
from app.dependencies.permission import RequirePermission
from app.constants.permissions import Permission
from app.common.responses import SuccessResponse, create_success_response

router = APIRouter()


@router.get(
    "/permissions",
    response_model=SuccessResponse[List[PermissionResponse]],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def list_permissions(db: Session = Depends(get_db)):
    perms = permission_repo.get_all(db)
    return create_success_response(data=perms, message="Permissions fetched")


@router.post(
    "/permissions/sync",
    response_model=SuccessResponse[dict],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def sync_permissions(db: Session = Depends(get_db)):
    count = sync_permissions_from_enum(db)
    return create_success_response(
        data={"synced": count}, message=f"Synced {count} permissions"
    )


@router.get(
    "/roles",
    response_model=SuccessResponse[List[RoleWithPermissions]],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def list_roles(db: Session = Depends(get_db)):
    roles = role_service.get_all_with_permissions(db)
    return create_success_response(data=roles, message="Roles fetched")


@router.post(
    "/roles",
    response_model=SuccessResponse[RoleResponse],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    role = role_service.create(db, role_in)
    return create_success_response(data=role, message="Role created")


@router.put(
    "/roles/{role_id}",
    response_model=SuccessResponse[RoleResponse],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def update_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    role = role_service.update(db, role_id, role_in)
    return create_success_response(data=role, message="Role updated")


@router.delete(
    "/roles/{role_id}",
    response_model=SuccessResponse[dict],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role_service.delete(db, role_id)
    return create_success_response(data=None, message="Role deleted")


@router.put(
    "/roles/{role_id}/permissions",
    response_model=SuccessResponse[dict],
    dependencies=[Depends(RequirePermission(Permission.ROLE_VIEW))],
)
def set_role_permissions(role_id: int, permission_ids: List[int], db: Session = Depends(get_db)):
    role_permission_repo.set_role_permissions(db, role_id, permission_ids)
    return create_success_response(data=None, message="Role permissions updated")
