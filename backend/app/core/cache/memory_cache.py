import time
import threading
from typing import Any, Dict, Optional, Tuple
from app.core.cache.base import CacheBackend


class MemoryCache(CacheBackend):
    def __init__(self, default_ttl: int = 300) -> None:
        self._default_ttl = default_ttl
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.RLock()

    async def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expiry = entry
            if expiry is not None and time.monotonic() > expiry:
                del self._store[key]
                return None
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self._lock:
            expiry: Optional[float] = None
            if ttl is None:
                ttl = self._default_ttl
            if ttl is not None and ttl > 0:
                expiry = time.monotonic() + ttl
            self._store[key] = (value, expiry)

    async def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    async def exists(self, key: str) -> bool:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return False
            value, expiry = entry
            if expiry is not None and time.monotonic() > expiry:
                del self._store[key]
                return False
            return True

    async def clear(self) -> None:
        with self._lock:
            self._store.clear()

    async def close(self) -> None:
        with self._lock:
            self._store.clear()
