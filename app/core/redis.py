import redis.asyncio as redis
from app.core.config import settings


redis_client = redis.from_url(settings.REDIS_URL)

async def check_redis_connection() ->bool:
    try:
        return await redis_client.ping()
    except Exception:
        return False

