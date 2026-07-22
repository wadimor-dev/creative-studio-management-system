from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repository import user_repo
from app.core.auth.password import verify_password
from app.core.auth.session import session_service
from app.core.exceptions import CSMSException
from app.core.auth.schemas import Token


class AuthService:
    def authenticate_user(
        self,
        db: Session,
        form_data: OAuth2PasswordRequestForm,
        ip_address: str = None,
        user_agent: str = None,
    ) -> tuple[Token, object]:
        user = user_repo.get_by_username(db, username=form_data.username)
        if not user:
            user = user_repo.get_by_email(db, email=form_data.username)
        if not user:
            raise CSMSException("Incorrect username or password", status_code=401)
        if not verify_password(form_data.password, user.hashed_password):
            raise CSMSException("Incorrect username or password", status_code=401)
        if not user.is_active:
            raise CSMSException("Inactive user", status_code=400)

        _, access_token, refresh_token = session_service.create_session(
            db=db,
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
        return token, user

    def refresh_token(self, db: Session, refresh_token_str: str) -> Token:
        access_token, new_refresh_token = session_service.refresh_session(
            db=db,
            refresh_token=refresh_token_str,
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )


auth_service = AuthService()
