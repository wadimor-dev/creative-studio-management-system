from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def create_access_token(subject: str | Any, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "role": role, "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str | Any, role: str) -> str:
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 # 30 days
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "role": role, "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
