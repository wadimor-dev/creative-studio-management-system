from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.auth.models import UserSession


class SessionRepository:
    def create(self, db: Session, **kwargs) -> UserSession:
        session = UserSession(**kwargs)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def get_by_refresh_token_hash(self, db: Session, token_hash: str) -> Optional[UserSession]:
        return db.query(UserSession).filter(
            UserSession.refresh_token_hash == token_hash,
            UserSession.is_revoked == False,
        ).first()

    def get_by_id(self, db: Session, session_id: int) -> Optional[UserSession]:
        return db.query(UserSession).filter(UserSession.id == session_id).first()

    def revoke(self, db: Session, session_id: int) -> Optional[UserSession]:
        session = self.get_by_id(db, session_id)
        if session:
            session.is_revoked = True
            session.revoked_at = datetime.utcnow()
            db.commit()
        return session

    def revoke_all_user_sessions(self, db: Session, user_id: int) -> None:
        db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_revoked == False,
        ).update({"is_revoked": True, "revoked_at": datetime.utcnow()})
        db.commit()

    def update_last_used(self, db: Session, session_id: int) -> None:
        db.query(UserSession).filter(UserSession.id == session_id).update(
            {"last_used_at": datetime.utcnow()}
        )
        db.commit()

    def rotate_token_hash(self, db: Session, session_id: int, new_hash: str) -> None:
        db.query(UserSession).filter(UserSession.id == session_id).update(
            {"refresh_token_hash": new_hash, "last_used_at": datetime.utcnow()}
        )
        db.commit()


session_repo = SessionRepository()
