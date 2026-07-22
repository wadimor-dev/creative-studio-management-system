import logging
from typing import List, Set
from sqlalchemy.orm import Session
from app.constants.permissions import Permission
from app.core.authorization.repositories import (
    permission_repo,
    role_permission_repo,
    user_role_repo,
    get_user_permissions,
)
from app.core.authorization.models import RolePermission

logger = logging.getLogger(__name__)


def sync_permissions_from_enum(db: Session) -> int:
    synced_count = 0
    for perm in Permission:
        parts = perm.value.split(".")
        module = parts[0] if len(parts) > 0 else None
        name = perm.value.replace(".", " ").title()
        try:
            existing = permission_repo.get_by_code(db, perm.value)
            if existing:
                existing.name = name
                if module:
                    existing.module = module
            else:
                from app.core.authorization.models import Permission as PermissionModel
                db.add(PermissionModel(code=perm.value, name=name, module=module))
            synced_count += 1
        except Exception as e:
            logger.error(f"Failed to sync permission {perm.value}: {e}")

    db.commit()
    logger.info(f"Synced {synced_count} permissions from enum to database")
    return synced_count


def sync_role_permissions_from_enum(db: Session) -> int:
    from app.constants.role_permissions import ROLE_PERMISSIONS
    from app.models.role import Role

    synced_count = 0

    for role_type, permissions in ROLE_PERMISSIONS.items():
        role_name = role_type.value if hasattr(role_type, 'value') else role_type
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            logger.warning(f"Role {role_name} not found in DB, skipping")
            continue

        existing_ids = role_permission_repo.get_role_permission_ids(db, role.id)
        target_ids: Set[int] = set()

        for perm in permissions:
            db_perm = permission_repo.get_by_code(db, perm.value)
            if db_perm:
                target_ids.add(db_perm.id)

        to_add = target_ids - existing_ids
        to_remove = existing_ids - target_ids

        for pid in to_add:
            db.add(RolePermission(role_id=role.id, permission_id=pid))
            synced_count += 1
        for pid in to_remove:
            db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == pid,
            ).delete()
            synced_count += 1

    db.commit()
    logger.info(f"Synced {synced_count} role-permission assignments")
    return synced_count


def set_user_roles(db: Session, user_id: int, role_ids: List[int]) -> None:
    user_role_repo.set_user_roles(db, user_id, role_ids)


def add_user_role(db: Session, user_id: int, role_id: int) -> None:
    user_role_repo.add_role_to_user(db, user_id, role_id)


def remove_user_role(db: Session, user_id: int, role_id: int) -> None:
    user_role_repo.remove_role_from_user(db, user_id, role_id)


def get_user_permission_set(db: Session, user_id: int) -> Set[str]:
    return get_user_permissions(db, user_id)
