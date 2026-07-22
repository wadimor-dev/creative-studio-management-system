from abc import ABC, abstractmethod
from typing import Any
from app.core.events.event import Event


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: Event) -> Any:
        raise NotImplementedError
