from app.core.authorization.models import Permission, RolePermission, UserRole
from app.core.authorization.schemas import PermissionResponse, RolePermissionResponse
from app.core.authorization.repositories import (
    PermissionRepository,
    RolePermissionRepository,
    UserRoleRepository,
    permission_repo,
    role_permission_repo,
    user_role_repo,
    get_user_permissions,
    get_user_roles,
)
from app.core.authorization.services import (
    sync_permissions_from_enum,
    sync_role_permissions_from_enum,
    set_user_roles,
    add_user_role,
    remove_user_role,
    get_user_permission_set,
)
from app.core.authorization.dependencies import (
    RequirePermission,
    OwnershipChecker,
    BranchChecker,
    ModuleChecker,
)

__all__ = [
    "Permission",
    "RolePermission",
    "UserRole",
    "PermissionResponse",
    "RolePermissionResponse",
    "PermissionRepository",
    "RolePermissionRepository",
    "UserRoleRepository",
    "permission_repo",
    "role_permission_repo",
    "user_role_repo",
    "get_user_permissions",
    "get_user_roles",
    "sync_permissions_from_enum",
    "sync_role_permissions_from_enum",
    "set_user_roles",
    "add_user_role",
    "remove_user_role",
    "get_user_permission_set",
    "RequirePermission",
    "OwnershipChecker",
    "BranchChecker",
    "ModuleChecker",
]
