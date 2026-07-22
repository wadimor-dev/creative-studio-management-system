from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Callable, Any

from app.core.database.session import get_db
from app.core.auth.dependencies import get_current_token_payload
from app.core.auth.schemas import TokenPayload
from app.core.authorization.repositories import get_user_permissions


class RequirePermission:
    def __init__(self, permission: str):
        self.permission = permission

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_token_payload),
    ) -> TokenPayload:
        if not token_payload.sub:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        try:
            user_id = int(token_payload.sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")

        permissions = getattr(request.state, "_permissions", None)
        if permissions is None:
            permissions = get_user_permissions(db, user_id)
            request.state._permissions = permissions

        if self.permission not in permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return token_payload


class OwnershipChecker:
    def __init__(self, get_owner_id: Callable[[Session, Any], int]):
        self.get_owner_id = get_owner_id

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_token_payload),
    ) -> None:
        if not token_payload.sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user_id = int(token_payload.sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")

        permissions = getattr(request.state, "_permissions", None)
        if permissions is None:
            permissions = get_user_permissions(db, user_id)
            request.state._permissions = permissions

        if "admin.override" in permissions:
            return

        resource_path = request.url.path
        resource_id = None
        for part in resource_path.split("/"):
            try:
                resource_id = int(part)
                break
            except (ValueError, TypeError):
                continue

        if resource_id is not None:
            owner_id = self.get_owner_id(db, resource_id)
            if owner_id and owner_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied: resource belongs to another user",
                )


class BranchChecker:
    def __init__(self, get_branch_id: Callable[[Session, Any], int]):
        self.get_branch_id = get_branch_id

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_token_payload),
    ) -> None:
        if not token_payload.sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user_id = int(token_payload.sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")

        permissions = getattr(request.state, "_permissions", None)
        if permissions is None:
            permissions = get_user_permissions(db, user_id)
            request.state._permissions = permissions

        if "admin.override" in permissions:
            return

        resource_path = request.url.path
        resource_id = None
        for part in resource_path.split("/"):
            try:
                resource_id = int(part)
                break
            except (ValueError, TypeError):
                continue

        if resource_id is not None:
            branch_id = self.get_branch_id(db, resource_id)
            if branch_id is not None:
                user_branch_id = getattr(request.state, "_user_branch_id", None)
                if user_branch_id is None:
                    from app.core.organization.employee.models import Employee
                    emp = db.query(Employee).filter(Employee.user_id == user_id).first()
                    if emp:
                        user_branch_id = emp.branch_id
                        request.state._user_branch_id = user_branch_id

                if user_branch_id and branch_id != user_branch_id:
                    raise HTTPException(
                        status_code=403,
                        detail="Access denied: resource belongs to a different branch",
                    )


class ModuleChecker:
    def __init__(self, module: str):
        self.module = module

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_token_payload),
    ) -> None:
        if not token_payload.sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user_id = int(token_payload.sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")

        permissions = getattr(request.state, "_permissions", None)
        if permissions is None:
            permissions = get_user_permissions(db, user_id)
            request.state._permissions = permissions

        has_module_access = any(p.startswith(f"{self.module}:") or p.startswith(f"{self.module}.") for p in permissions)
        if not has_module_access:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: no permissions for module '{self.module}'",
            )
