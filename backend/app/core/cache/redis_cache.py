import json
import logging
from typing import Any, Optional
from app.core.cache.base import CacheBackend

logger = logging.getLogger(__name__)


class RedisCache(CacheBackend):
    def __init__(self, redis_url: str, default_ttl: int = 300) -> None:
        self._redis_url = redis_url
        self._default_ttl = default_ttl
        self._client: Optional[Any] = None

    @property
    async def client(self) -> Any:
        if self._client is None:
            import redis.asyncio as aioredis
            self._client = aioredis.from_url(
                self._redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            try:
                await self._client.ping()
                logger.info("Connected to Redis at %s", self._redis_url)
            except Exception:
                logger.warning("Redis unavailable, falling back to degraded mode")
                self._client = None
                raise
        return self._client

    async def get(self, key: str) -> Optional[Any]:
        try:
            c = await self.client
            raw = await c.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception:
            logger.exception("Redis get failed for key %s", key)
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        try:
            c = await self.client
            raw = json.dumps(value, default=str)
            if ttl is None:
                ttl = self._default_ttl
            await c.set(key, raw, ex=ttl if ttl > 0 else None)
        except Exception:
            logger.exception("Redis set failed for key %s", key)

    async def delete(self, key: str) -> bool:
        try:
            c = await self.client
            result = await c.delete(key)
            return result > 0
        except Exception:
            logger.exception("Redis delete failed for key %s", key)
            return False

    async def exists(self, key: str) -> bool:
        try:
            c = await self.client
            return await c.exists(key) > 0
        except Exception:
            logger.exception("Redis exists failed for key %s", key)
            return False

    async def clear(self) -> None:
        try:
            c = await self.client
            await c.flushdb()
        except Exception:
            logger.exception("Redis clear failed")

    async def close(self) -> None:
        if self._client is not None:
            try:
                await self._client.close()
            except Exception:
                logger.exception("Redis close failed")
            finally:
                self._client = None
