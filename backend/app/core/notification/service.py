import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.notification.models import (
    Notification, NotificationChannel, NotificationStatus,
)
from app.core.notification.schemas import NotificationCreate
from app.core.notification.channels.base import NotificationChannelBase
from app.core.notification.channels.in_app import InAppChannel
from app.core.notification.channels.email import EmailChannel
from app.core.database.helpers import jakarta_now, get_or_404
from app.core.events import event_dispatcher, Event
from app.models.user import User

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self) -> None:
        self._channels: Dict[str, NotificationChannelBase] = {}

    def register_channel(self, channel: NotificationChannelBase) -> None:
        self._channels[channel.channel_type] = channel
        logger.info("Notification channel registered: %s", channel.channel_type)

    async def send(
        self,
        db: Session,
        user_id: int,
        title: str,
        body: Optional[str] = None,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        reference_type: Optional[str] = None,
        reference_id: Optional[int] = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            channel=channel,
            title=title,
            body=body,
            status=NotificationStatus.PENDING,
            reference_type=reference_type,
            reference_id=reference_id,
            created_at=jakarta_now(),
        )
        db.add(notification)
        db.flush()

        channel_impl = self._channels.get(channel.value)
        if channel_impl:
            success = await channel_impl.send(notification)
            if not success:
                notification.status = NotificationStatus.FAILED
                notification.error_message = "Channel delivery failed"
        else:
            notification.status = NotificationStatus.SENT
            notification.sent_at = jakarta_now()

        db.commit()
        db.refresh(notification)

        await event_dispatcher.dispatch(
            Event(
                name="notification.sent",
                data={
                    "notification_id": notification.id,
                    "user_id": user_id,
                    "title": title,
                    "channel": channel.value,
                },
            )
        )

        return notification

    async def send_to_multiple(
        self,
        db: Session,
        user_ids: List[int],
        title: str,
        body: Optional[str] = None,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        reference_type: Optional[str] = None,
        reference_id: Optional[int] = None,
    ) -> List[Notification]:
        results: List[Notification] = []
        for uid in user_ids:
            notif = await self.send(
                db=db, user_id=uid, title=title, body=body,
                channel=channel, reference_type=reference_type,
                reference_id=reference_id,
            )
            results.append(notif)
        return results

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Notification]:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()

    def get_unread_count(self, db: Session, user_id: int) -> int:
        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
        ).count()

    def mark_as_read(self, db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
        notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        ).first()
        if not notif:
            return None
        notif.is_read = True
        notif.status = NotificationStatus.READ
        notif.read_at = jakarta_now()
        db.commit()
        db.refresh(notif)
        return notif

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        now = jakarta_now()
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
        ).update(
            {"is_read": True, "status": NotificationStatus.READ, "read_at": now},
            synchronize_session=False,
        )
        db.commit()
        return count

    def mark_multiple_as_read(self, db: Session, ids: List[int], user_id: int) -> int:
        now = jakarta_now()
        count = db.query(Notification).filter(
            Notification.id.in_(ids),
            Notification.user_id == user_id,
        ).update(
            {"is_read": True, "status": NotificationStatus.READ, "read_at": now},
            synchronize_session=False,
        )
        db.commit()
        return count
