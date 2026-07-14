from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.session import get_db
from app.core.jwt import ALGORITHM, decode_access_token
from app.schemas.auth import TokenPayload
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)
        logger.debug(f"✅ Token validated - User: {token_data.sub}, Role: {token_data.role}")
    except JWTError as e:
        logger.warning(f"❌ Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def get_current_user(
    db: Session = Depends(get_db),
    token_payload: TokenPayload = Depends(get_current_token_payload)
):
    from app.repositories.user_repository import user_repo
    user = user_repo.get_by_username(db, token_payload.sub)
    if not user:
        logger.warning(f"❌ User not found: {token_payload.sub}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
