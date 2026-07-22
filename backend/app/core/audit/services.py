from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog
from app.models.audit_log import AuditLog


class LoggerService:
    @staticmethod
    def log_activity(
        db: Session,
        user_id: Optional[int],
        action_type: str,
        description: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ActivityLog:
        log = ActivityLog(
            user_id=user_id,
            action_type=action_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def log_audit(
        db: Session,
        user_id: Optional[int],
        table_name: str,
        record_id: int,
        action: str,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        audit = AuditLog(
            user_id=user_id,
            table_name=table_name,
            record_id=record_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit


logger_service = LoggerService()
