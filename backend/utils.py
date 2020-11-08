import aioredis

from consts import REDIS_URL


async def put_to_redis(key: str, value: str) -> None:
    redis = await aioredis.create_redis_pool(REDIS_URL)
    await redis.set(key, value)
    redis.close()
    await redis.wait_closed()


async def get_from_redis(key: str) -> bytes:
    redis = await aioredis.create_redis_pool(REDIS_URL)
    value = await redis.get(key)
    return value
