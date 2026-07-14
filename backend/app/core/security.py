from typing import Any, List

class RoleChecker:
    @staticmethod
    def is_allowed(current_role: str, allowed_roles: List[str]) -> bool:
        return current_role in allowed_roles

class PermissionChecker:
    @staticmethod
    def has_permission(current_permissions: List[str], required_permission: str) -> bool:
        return required_permission in current_permissions

class OwnershipChecker:
    @staticmethod
    def is_owner(current_user_id: Any, resource_owner_id: Any) -> bool:
        return str(current_user_id) == str(resource_owner_id)
