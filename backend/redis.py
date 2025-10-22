from __future__ import annotations
import builtins
import logging
from typing import Any
import os

import redis.asyncio as redis

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# redis://[:password]@host:port/db
# redis:// → regular Redis connection
# rediss:// → SSL/TLS connection (secure)
# :password@ → optional authentication
# /db → optional DB index (see below)

# TODO: May want to add group/tenant in the future tenant:session:user: etc...

# TODO: Adding a connect method may be ideal as well


class RedisAdapter:
    """
    Async wrapper for Redis operations, supporting common key-value and set methods.
    Used for caching, sessions, locking, and more.
    """

    def __init__(self, url: str = REDIS_URL):
        self.conn: redis.Redis = redis.Redis.from_url(url, decode_responses=True)
        # redis.Redis(host="localhost", port=6379, db=2)

    async def set(self, key: str, val: Any, ex: int = 3600, nx: bool = False) -> bool:
        """
        Store a value in Redis with optional expiry.

        Args:
            key (str): The Redis key.
            val (Any): The value to store. Should be JSON-serializable.
            expiry (int): Expiry in seconds (default: 3600).

        Note:
            Allow keyword instantiation in future iterations.

        Returns:
            bool: True if successful.
        """
        try:
            result = await self.conn.set(key, val, ex=ex, nx=nx)
            return result is True
        except Exception as e:
            logger.error("Redis SET failed for key '%s': %s", key, str(e))
            raise

    async def get(self, key: str) -> str | None:
        """
        Retrieve a value from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            (str | None): The stored value or None.
        """
        try:
            return await self.conn.get(key)
        except Exception as e:
            logger.error("Redis GET failed for key '%s': %s", key, str(e))
            raise

    async def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            bool: The stored value or None.
        """
        try:
            deleted_count = await self.conn.delete(key)
            return deleted_count > 0
        except Exception as e:
            logger.error("Redis DELETE failed for key '%s': %s", key, str(e))
            raise

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists.

        Args:
            key (str): The Redis key.

        Returns:
            bool: The stored value or None.
        """
        try:
            return await self.conn.exists(key) > 0
        except Exception as e:
            logger.error("Redis EXISTS failed for key '%s': %s", key, str(e))
            raise

    async def incr(self, key: str) -> int:
        """
        Atomically increment the integer value of a key.

        Args:
            key (str): The Redis key.

        Returns:
            bool: The stored value or None.
        """

        # val = await self.get(key)
        # if val is None:
        #     await self.set(key, -1)

        try:
            return await self.conn.incr(key)
        except Exception as e:
            logger.error("Redis INCR failed for key '%s': %s", key, str(e))
            raise

    async def sadd(self, key: str, *values: str) -> int:
        """
        Add one or more members to a Redis set.

        Args:
            key (str): The Redis key.
            *values (str): Values to add to the set

        Returns:
            int: Number of keys added to the set
        """
        try:
            return await self.conn.sadd(key, *values)
        except Exception as e:
            logger.error("Redis SADD failed for key '%s': %s", key, str(e))
            raise

    async def sismember(self, key: str, val: str) -> bool:
        """Check if a value is a member of the set at key."""
        try:
            return bool(await self.conn.sismember(key, val))
        except Exception as e:
            logger.error("Redis SISMEMBER failed for key '%s': %s", key, str(e))
            raise

    async def smembers(self, key: str) -> builtins.set[str]:
        """Get all members of the set at key."""
        try:
            members = await self.conn.smembers(key)
            return {m if isinstance(m, str) else m.decode() for m in members}
        except Exception as e:
            logger.error("Redis SMEMBERS failed for key '%s': %s", key, str(e))
            raise

    async def acquire_lock(self, key: str, ttl: int) -> bool:
        """Try to acquire a distributed lock on a key."""
        try:
            return await self.conn.set(key, "1", nx=True, ex=ttl) is True
        except Exception as e:
            logger.error("Redis LOCK acquisition failed for key '%s': %s", key, str(e))
            raise

    async def release_lock(self, key: str) -> None:
        """Release a distributed lock."""
        try:
            await self.conn.delete(key)
        except Exception as e:
            logger.error("Redis LOCK release failed for key '%s': %s", key, str(e))
            raise

    async def keys(self, pattern: str = "*") -> list[str]:
        """Return all keys matching a given pattern."""
        try:
            keys = await self.conn.keys(pattern)
            return [k if isinstance(k, str) else k.decode() for k in keys]
        except Exception as e:
            logger.error("Redis KEYS failed for pattern '%s': %s", pattern, str(e))
            raise

    async def query(self, pattern: str) -> list[str]:
        """
        Query a pattern using the scan method. More efficient than keys.
        """
        cursor = 0
        keys = []
        while True:
            cursor, chunk = await self.conn.scan(cursor=cursor, match=pattern, count=50)
            keys.extend(chunk)
            if cursor == 0:
                break
        return keys

    async def flush(self) -> None:
        """
        Removes all contents of the database.
        """
        await self.conn.flushdb()

    async def close(self) -> None:
        """
        Closes connection to the database.
        """
        await self.conn.aclose()