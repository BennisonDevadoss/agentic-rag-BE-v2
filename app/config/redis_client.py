import redis.asyncio as redis

from config.settings import SETTINGS

redis_client = redis.from_url(SETTINGS.REDIS_BASE_URL, decode_responses=True)
