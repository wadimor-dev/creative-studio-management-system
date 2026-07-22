from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.services.auth_service import auth_service
from app.core.audit.services import logger_service
from app.common.responses import SuccessResponse, create_success_response
from app.core.auth.schemas import Token, RefreshRequest
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user
from app.repositories.user_repository import user_repo
from app.core.exceptions import CSMSException
from app.core.auth.session import session_service

router = APIRouter()


@router.post("/login", response_model=SuccessResponse[Token])
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    token_data, user = auth_service.authenticate_user(
        db, form_data, ip_address=ip_address, user_agent=user_agent
    )

    try:
        logger_service.log_activity(
            db=db,
            user_id=user.id,
            action_type="LOGIN",
            description="User logged in",
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception:
        pass

    return create_success_response(data=token_data, message="Login successful")


@router.post("/refresh", response_model=SuccessResponse[Token])
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    token_data = auth_service.refresh_token(db, request.refresh_token)
    return create_success_response(data=token_data, message="Token refreshed successfully")


@router.post("/logout", response_model=SuccessResponse[dict])
def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token_str = auth_header[7:]
        session_service.revoke_session(db, token_str)

    return create_success_response(data=None, message="Logout successful")


@router.post("/logout/all", response_model=SuccessResponse[dict])
def logout_all(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session_service.revoke_all_user_sessions(db, current_user.id)
    return create_success_response(data=None, message="All sessions revoked")


@router.get("/me", response_model=SuccessResponse[UserResponse])
def get_current_user_info(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    user = user_repo.get_by_id_with_roles(db, current_user.id)
    if not user:
        raise CSMSException("User not found", status_code=404)
    return create_success_response(data=user, message="Current user fetched successfully")
