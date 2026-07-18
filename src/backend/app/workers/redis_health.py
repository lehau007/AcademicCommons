from redis.asyncio import Redis


async def check_redis(redis_url: str) -> str:
    client = Redis.from_url(redis_url)
    try:
        await client.ping()
    except Exception:
        return "unavailable"
    finally:
        await client.aclose()
    return "ok"

