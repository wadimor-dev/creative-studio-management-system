from typing import Optional
from sqlalchemy.orm import Session
import uuid

from app.core.database.helpers import (  # noqa: F401
    jakarta_now, jakarta_today, get_or_404, validate_quantity,
    acquire_stock_lock, get_or_create_stock, update_stock_with_optimistic_lock,
)


def log_activity(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int,
    user_id: int = None,
    actor_type: str = "USER",
    request_id: str = None,
    idempotency_key: str = None,
    detail: str = None,
    old_value: str = None,
    new_value: str = None,
):
    from app.models.showroom_activity_log import ShowroomActivityLog

    if not request_id:
        request_id = str(uuid.uuid4())

    log = ShowroomActivityLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=user_id,
        actor_type=actor_type,
        request_id=request_id,
        idempotency_key=idempotency_key,
        detail=detail,
        old_value=old_value,
        new_value=new_value,
        created_at=jakarta_now(),
    )
    db.add(log)
    return log
