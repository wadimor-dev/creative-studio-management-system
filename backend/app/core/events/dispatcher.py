import asyncio
import logging
from typing import Any, Dict, List, Optional, Type
from app.core.events.event import Event
from app.core.events.handler import EventHandler

logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}

    def register(self, event_name: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_name, []).append(handler)
        logger.debug("Handler %s registered for event %s", handler.__class__.__name__, event_name)

    def unregister(self, event_name: str, handler: EventHandler) -> None:
        handlers = self._handlers.get(event_name)
        if handlers:
            handlers[:] = [h for h in handlers if h is not handler]
            logger.debug("Handler %s unregistered from event %s", handler.__class__.__name__, event_name)

    def unregister_all(self, event_name: Optional[str] = None) -> None:
        if event_name:
            self._handlers.pop(event_name, None)
        else:
            self._handlers.clear()

    async def dispatch(self, event: Event) -> List[Any]:
        handlers = self._handlers.get(event.name, [])
        if not handlers:
            logger.debug("No handlers registered for event %s", event.name)
            return []

        results: List[Any] = []
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler.handle):
                    result = await handler.handle(event)
                else:
                    result = handler.handle(event)
                results.append(result)
            except Exception:
                logger.exception(
                    "Handler %s failed for event %s",
                    handler.__class__.__name__, event.name,
                )
        return results

    def dispatch_sync(self, event: Event) -> List[Any]:
        handlers = self._handlers.get(event.name, [])
        if not handlers:
            return []

        results: List[Any] = []
        for handler in handlers:
            try:
                results.append(handler.handle(event))
            except Exception:
                logger.exception(
                    "Handler %s failed for event %s",
                    handler.__class__.__name__, event.name,
                )
        return results

    def has_handlers(self, event_name: str) -> bool:
        return bool(self._handlers.get(event_name))
