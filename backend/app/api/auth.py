from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.session import get_db
from app.services.auth_service import auth_service
from app.common.responses import SuccessResponse, create_success_response
from app.schemas.auth import Token, TokenPayload
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_token_payload
from app.repositories.user_repository import user_repo
from app.exceptions.base import CSMSException

router = APIRouter()

@router.post("/login", response_model=SuccessResponse[Token])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token_data = auth_service.authenticate_user(db, form_data)
    return create_success_response(data=token_data, message="Login successful")

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=SuccessResponse[Token])
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    token_data = auth_service.refresh_token(db, request.refresh_token)
    return create_success_response(data=token_data, message="Token refreshed successfully")

@router.post("/logout", response_model=SuccessResponse[dict])
def logout():
    return create_success_response(data=None, message="Logout successful (clear token on client)")

@router.get("/me", response_model=SuccessResponse[UserResponse])
def get_current_user(
    db: Session = Depends(get_db),
    token_payload: TokenPayload = Depends(get_current_token_payload)
):
    user = user_repo.get_by_username(db, token_payload.sub)
    if not user:
        raise CSMSException("User not found", status_code=404)
    return create_success_response(data=user, message="Current user fetched successfully")
