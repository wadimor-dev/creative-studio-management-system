from typing import List, Optional, Set
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.authorization.models import Permission


class PermissionRepository:
    def get_by_code(self, db: Session, code: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.code == code).first()

    def get_all(self, db: Session) -> List[Permission]:
        return db.query(Permission).order_by(Permission.module, Permission.code).all()

    def get_by_module(self, db: Session, module: str) -> List[Permission]:
        return db.query(Permission).filter(Permission.module == module).all()

    def upsert(self, db: Session, code: str, name: str, module: str = None, description: str = None) -> Permission:
        perm = self.get_by_code(db, code)
        if perm:
            perm.name = name
            if module is not None:
                perm.module = module
            if description is not None:
                perm.description = description
        else:
            perm = Permission(code=code, name=name, module=module, description=description)
            db.add(perm)
        db.commit()
        db.refresh(perm)
        return perm

    def delete(self, db: Session, permission_id: int) -> None:
        db.query(Permission).filter(Permission.id == permission_id).delete()
        db.commit()


class RolePermissionRepository:
    def get_role_permission_ids(self, db: Session, role_id: int) -> Set[int]:
        from app.core.authorization.models import RolePermission
        rows = db.query(RolePermission.permission_id).filter(
            RolePermission.role_id == role_id
        ).all()
        return {r[0] for r in rows}

    def set_role_permissions(self, db: Session, role_id: int, permission_ids: List[int]) -> None:
        from app.core.authorization.models import RolePermission
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        for pid in permission_ids:
            db.add(RolePermission(role_id=role_id, permission_id=pid))
        db.commit()

    def add_permission_to_role(self, db: Session, role_id: int, permission_id: int) -> None:
        from app.core.authorization.models import RolePermission
        existing = db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        ).first()
        if not existing:
            db.add(RolePermission(role_id=role_id, permission_id=permission_id))
            db.commit()

    def remove_permission_from_role(self, db: Session, role_id: int, permission_id: int) -> None:
        from app.core.authorization.models import RolePermission
        db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        ).delete()
        db.commit()


class UserRoleRepository:
    def get_user_role_ids(self, db: Session, user_id: int) -> List[int]:
        from app.core.authorization.models import UserRole
        rows = db.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()
        return [r[0] for r in rows]

    def set_user_roles(self, db: Session, user_id: int, role_ids: List[int]) -> None:
        from app.core.authorization.models import UserRole
        db.query(UserRole).filter(UserRole.user_id == user_id).delete()
        for rid in role_ids:
            db.add(UserRole(user_id=user_id, role_id=rid))
        db.commit()

    def add_role_to_user(self, db: Session, user_id: int, role_id: int) -> None:
        from app.core.authorization.models import UserRole
        existing = db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        ).first()
        if not existing:
            db.add(UserRole(user_id=user_id, role_id=role_id))
            db.commit()

    def remove_role_from_user(self, db: Session, user_id: int, role_id: int) -> None:
        from app.core.authorization.models import UserRole
        db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        ).delete()
        db.commit()


def get_user_permissions(db: Session, user_id: int) -> Set[str]:
    sql = text("""
        SELECT DISTINCT p.code
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        JOIN user_roles ur ON ur.role_id = rp.role_id
        WHERE ur.user_id = :user_id
    """)
    rows = db.execute(sql, {"user_id": user_id}).fetchall()
    return {row[0] for row in rows}


def get_user_roles(db: Session, user_id: int) -> List:
    from app.models.role import Role
    role_ids = user_role_repo.get_user_role_ids(db, user_id)
    if not role_ids:
        return []
    return db.query(Role).filter(Role.id.in_(role_ids)).all()


permission_repo = PermissionRepository()
role_permission_repo = RolePermissionRepository()
user_role_repo = UserRoleRepository()
