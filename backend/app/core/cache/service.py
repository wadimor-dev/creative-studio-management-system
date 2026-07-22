import logging
from typing import Any, Callable, Optional, TypeVar

from app.core.cache.base import CacheBackend
from app.core.cache.memory_cache import MemoryCache
from app.core.cache.redis_cache import RedisCache
from app.core.config import settings

T = TypeVar("T")
logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self) -> None:
        self._backend: Optional[CacheBackend] = None
        self._initialized = False

    async def initialize(self) -> None:
        if self._initialized:
            return

        if settings.REDIS_URL:
            self._backend = RedisCache(
                redis_url=settings.REDIS_URL,
                default_ttl=settings.CACHE_DEFAULT_TTL,
            )
            try:
                await self._backend.client
                logger.info("Cache backend: Redis")
            except Exception:
                logger.warning("Redis unavailable, falling back to MemoryCache")
                self._backend = MemoryCache(default_ttl=settings.CACHE_DEFAULT_TTL)
        else:
            self._backend = MemoryCache(default_ttl=settings.CACHE_DEFAULT_TTL)
            logger.info("Cache backend: Memory (no REDIS_URL configured)")

        self._initialized = True

    @property
    def backend(self) -> CacheBackend:
        if self._backend is None:
            self._backend = MemoryCache(default_ttl=300)
        return self._backend

    async def get(self, key: str) -> Any:
        return await self.backend.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        await self.backend.set(key, value, ttl)

    async def delete(self, key: str) -> bool:
        return await self.backend.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.backend.exists(key)

    async def clear(self) -> None:
        await self.backend.clear()

    async def close(self) -> None:
        if self._backend is not None:
            await self._backend.close()
        self._initialized = False

    async def remember(self, key: str, ttl: int, factory: Callable[[], T]) -> T:
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = factory()
        await self.set(key, value, ttl)
        return value

    async def remember_async(self, key: str, ttl: int, factory: Callable[[], T]) -> T:
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = await factory()
        await self.set(key, value, ttl)
        return value

    def key(self, *parts: str) -> str:
        return ":".join(parts)
