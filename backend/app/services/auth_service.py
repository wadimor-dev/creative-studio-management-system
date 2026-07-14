from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repository import user_repo
from app.core.password import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.exceptions.base import CSMSException
from app.schemas.auth import Token

class AuthService:
    def authenticate_user(self, db: Session, form_data: OAuth2PasswordRequestForm) -> Token:
        user = user_repo.get_by_username(db, username=form_data.username)
        if not user:
            user = user_repo.get_by_email(db, email=form_data.username)
        if not user:
            raise CSMSException("Incorrect username or password", status_code=401)
        if not verify_password(form_data.password, user.hashed_password):
            raise CSMSException("Incorrect username or password", status_code=401)
        if not user.is_active:
            raise CSMSException("Inactive user", status_code=400)
            
        # Normalize role to UPPERCASE for consistency
        role_name = user.role.name.upper() if user.role else "STAFF"
        access_token = create_access_token(subject=user.username, role=role_name)
        refresh_token = create_refresh_token(subject=user.username, role=role_name)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    def refresh_token(self, db: Session, refresh_token: str) -> Token:
        from app.core.jwt import decode_access_token
        from jose import JWTError
        try:
            payload = decode_access_token(refresh_token)
            if payload.get("type") != "refresh":
                raise CSMSException("Invalid token type", status_code=401)
            username = payload.get("sub")
        except JWTError:
            raise CSMSException("Could not validate credentials", status_code=401)
            
        user = user_repo.get_by_username(db, username=username)
        if not user or not user.is_active:
            raise CSMSException("User not found or inactive", status_code=401)
            
        role_name = user.role.name if user.role else "STAFF"
        new_access_token = create_access_token(subject=user.username, role=role_name)
        new_refresh_token = create_refresh_token(subject=user.username, role=role_name)
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

auth_service = AuthService()
