import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session as DBSession
from app.core.auth.models import UserSession
from app.core.auth.repositories import session_repo
from app.core.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.core.exceptions import CSMSException


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _utcnow():
    return datetime.utcnow()


class SessionService:
    def create_session(
        self,
        db: DBSession,
        user_id: int,
        device: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[UserSession, str, str]:
        now = _utcnow()

        session = session_repo.create(
            db,
            user_id=user_id,
            refresh_token_hash="",
            device=device,
            ip_address=ip_address,
            user_agent=user_agent,
            expired_at=now + timedelta(days=30),
        )

        access_token = create_access_token(
            subject=user_id,
            session_id=str(session.id),
        )
        refresh_token = create_refresh_token(
            subject=user_id,
            session_id=str(session.id),
        )
        token_hash = _hash_token(refresh_token)
        session_repo.rotate_token_hash(db, session.id, token_hash)

        return session, access_token, refresh_token

    def refresh_session(
        self,
        db: DBSession,
        refresh_token: str,
    ) -> Tuple[str, str]:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise CSMSException("Invalid token type", status_code=401)

            session_id = payload.get("session_id")
            if not session_id:
                raise CSMSException("Invalid token payload", status_code=401)

            try:
                session_id = int(session_id)
            except (ValueError, TypeError):
                raise CSMSException("Invalid session in token", status_code=401)

            session = session_repo.get_by_id(db, session_id)
            if not session:
                raise CSMSException("Session not found", status_code=401)
            if session.is_revoked:
                raise CSMSException("Session has been revoked", status_code=401)
            if session.expired_at and session.expired_at < _utcnow():
                raise CSMSException("Session expired", status_code=401)

            token_hash = _hash_token(refresh_token)
            if session.refresh_token_hash != token_hash:
                raise CSMSException("Invalid refresh token", status_code=401)

            new_access_token = create_access_token(
                subject=session.user_id,
                session_id=str(session.id),
            )
            new_refresh_token_str = str(uuid.uuid4())
            new_token_hash = _hash_token(new_refresh_token_str)

            session_repo.rotate_token_hash(db, session.id, new_token_hash)

            return new_access_token, new_refresh_token_str

        except CSMSException:
            raise
        except Exception:
            raise CSMSException("Could not validate credentials", status_code=401)

    def revoke_session(self, db: DBSession, access_token: str) -> None:
        try:
            payload = decode_token(access_token)
            session_id = payload.get("session_id")
            if session_id:
                try:
                    session_repo.revoke(db, int(session_id))
                except (ValueError, TypeError):
                    pass
        except Exception:
            pass

    def revoke_all_user_sessions(self, db: DBSession, user_id: int) -> None:
        session_repo.revoke_all_user_sessions(db, user_id)


session_service = SessionService()
