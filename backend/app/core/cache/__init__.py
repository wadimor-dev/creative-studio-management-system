from app.core.cache.base import CacheBackend
from app.core.cache.memory_cache import MemoryCache
from app.core.cache.redis_cache import RedisCache
from app.core.cache.service import CacheService

cache_service = CacheService()

__all__ = [
    "CacheBackend",
    "MemoryCache",
    "RedisCache",
    "CacheService",
    "cache_service",
]
