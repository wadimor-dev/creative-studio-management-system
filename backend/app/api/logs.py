from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Any
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.activity_log import ActivityLog
from app.models.audit_log import AuditLog
from app.models.user import User

router = APIRouter()

@router.get("/activity", summary="Get activity logs")
def get_activity_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    skip: int = 0
) -> Any:
    """Retrieve activity logs, descending order."""
    # Ensure only superadmin/admin can see logs if needed
    # (Assuming deps.get_current_active_user suffices for now)
    logs = db.query(ActivityLog).order_by(desc(ActivityLog.created_at)).offset(skip).limit(limit).all()
    
    # We need to serialize with user info
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "user": log.user.username if log.user else "System",
            "action_type": log.action_type,
            "description": log.description,
            "ip_address": log.ip_address,
            "created_at": log.created_at
        })
    return {"data": result}

@router.get("/audit", summary="Get audit logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    skip: int = 0
) -> Any:
    """Retrieve audit logs, descending order."""
    logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "user": log.user.username if log.user else "System",
            "table_name": log.table_name,
            "record_id": log.record_id,
            "action": log.action,
            "old_value": log.old_value,
            "new_value": log.new_value,
            "created_at": log.created_at
        })
    return {"data": result}
