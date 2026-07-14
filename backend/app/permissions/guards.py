from fastapi import HTTPException, status
from app.schemas.auth import TokenPayload
import logging

logger = logging.getLogger(__name__)

def check_role_access(token_payload: TokenPayload, allowed_roles: list[str]) -> bool:
    """
    Check if user's role is in allowed_roles.
    Both token_payload.role and allowed_roles should be in UPPERCASE.
    """
    user_role = token_payload.role.upper() if token_payload.role else None
    allowed_roles_upper = [r.upper() for r in allowed_roles]
    
    if not user_role or user_role not in allowed_roles_upper:
        logger.warning(
            f"❌ Permission denied - User: {token_payload.sub}, "
            f"Role: {token_payload.role}, Allowed: {allowed_roles}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operation not permitted. Required roles: {', '.join(allowed_roles)}"
        )
    
    logger.debug(f"✅ Permission granted - User: {token_payload.sub}, Role: {token_payload.role}")
    return True
