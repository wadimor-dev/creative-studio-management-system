from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.showroom_permission import ShowroomUserRole, showroom_role_permissions, ShowroomPermission
from app.models.user import User


def get_user_permissions(db: Session, user_id: int) -> set:
    rows = (
        db.query(ShowroomPermission.code)
        .join(showroom_role_permissions, showroom_role_permissions.c.permission_id == ShowroomPermission.id)
        .join(ShowroomUserRole, ShowroomUserRole.role_id == showroom_role_permissions.c.role_id)
        .filter(ShowroomUserRole.user_id == user_id)
        .distinct()
        .all()
    )
    return {r[0] for r in rows}


def has_permission(db: Session, user_id: int, permission_code: str) -> bool:
    perms = get_user_permissions(db, user_id)
    if "SHOWROOM_ADMIN" in perms:
        return True
    return permission_code in perms


def require_permission(permission_code: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, db: Session = None, current_user: User = None, **kwargs):
            if not db or not current_user:
                raise HTTPException(status_code=500, detail="Missing db or current_user")
            if not has_permission(db, current_user.id, permission_code):
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: requires {permission_code}",
                )
            return func(*args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def require_any_permission(*permission_codes: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, db: Session = None, current_user: User = None, **kwargs):
            if not db or not current_user:
                raise HTTPException(status_code=500, detail="Missing db or current_user")
            perms = get_user_permissions(db, current_user.id)
            if "SHOWROOM_ADMIN" in perms:
                return func(*args, db=db, current_user=current_user, **kwargs)
            if not any(p in perms for p in permission_codes):
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: requires one of {', '.join(permission_codes)}",
                )
            return func(*args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator
