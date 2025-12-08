import os

import redis.asyncio as redis


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379",
)


redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


async def check_redis() -> bool:

    try:
        return await redis_client.ping()
    except redis.RedisError:
        return False