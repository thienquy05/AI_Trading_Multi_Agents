from collections.abc import Iterator

import redis

from app.config import get_settings

# One process-wide pool; connections are returned to it when each
# per-request client is released.
_pool: redis.ConnectionPool | None = None


def _get_pool() -> redis.ConnectionPool:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = redis.ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
            # redis-py's default is *no* timeout — a dead Redis would hang
            # the login path forever. Fail fast (500) instead.
            socket_connect_timeout=3,
            socket_timeout=3,
        )
    return _pool


def get_redis() -> Iterator[redis.Redis]:
    """FastAPI dependency — tests override this with fakeredis."""
    client = redis.Redis(connection_pool=_get_pool())
    try:
        yield client
    finally:
        client.close()
