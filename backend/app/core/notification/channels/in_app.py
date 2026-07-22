import logging
from typing import Any
from sqlalchemy.orm import Session
from app.core.notification.channels.base import NotificationChannelBase
from app.core.notification.models import Notification, NotificationStatus
from app.core.database.helpers import jakarta_now

logger = logging.getLogger(__name__)


class InAppChannel(NotificationChannelBase):
    @property
    def channel_type(self) -> str:
        return "in_app"

    async def send(self, notification: Notification, context: Any = None) -> bool:
        try:
            notification.status = NotificationStatus.SENT
            notification.sent_at = jakarta_now()
            logger.debug("In-app notification %s marked as sent", notification.id)
            return True
        except Exception:
            logger.exception("Failed to send in-app notification %s", notification.id)
            return False
