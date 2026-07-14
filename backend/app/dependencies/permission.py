from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_token_payload
from app.schemas.auth import TokenPayload

from app.constants.role_permissions import ROLE_PERMISSIONS


class RequirePermission:

    def __init__(self, permission):
        self.permission = permission

    def __call__(
        self,
        token_payload: TokenPayload = Depends(get_current_token_payload)
    ):

        permissions = ROLE_PERMISSIONS.get(
            token_payload.role,
            set()
        )

        if self.permission not in permissions:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return token_payload