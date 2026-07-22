from app.core.notification.models import Notification, NotificationChannel, NotificationStatus
from app.core.notification.service import NotificationService

notification_service = NotificationService()

__all__ = [
    "Notification",
    "NotificationChannel",
    "NotificationStatus",
    "NotificationService",
    "notification_service",
]
