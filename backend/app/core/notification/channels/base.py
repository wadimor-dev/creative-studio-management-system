from abc import ABC, abstractmethod
from typing import Any
from app.core.notification.models import Notification


class NotificationChannelBase(ABC):
    @abstractmethod
    async def send(self, notification: Notification, context: Any = None) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def channel_type(self) -> str:
        raise NotImplementedError
