

import logging

logger = logging.getLogger(__name__)

class AnalysisRedisRepository:
    def __init__(self):
        pass
    def cache_key(parcel_id: int, persona: str, ordinance_version: str, prompt_version: str) -> str:
        return f"{CACHE_PREFIX}:{parcel_id}:{persona}:{ordinance_version}:{prompt_version}"
    async def _cache_get(redis: Redis, key: str) -> AnalysisResponse | None:
        try:
            raw = await redis.get(key)
        except RedisError:
            logger.warning("Redis GET failed for %s", key, exc_info=True)
            return None
        if raw is None:
            return None
        try:
            return AnalysisResponse.model_validate_json(raw)
        except ValueError:
            # Schema changed or corrupt entry: treat as a miss and drop it
            logger.warning("Invalid cached analysis at %s, evicting", key)
            try:
                await redis.delete(key)
            except RedisError:
                pass
            return None
    async def _cache_set(redis: Redis, key: str, response: AnalysisResponse) -> None:
        try:
            await redis.set(key, response.model_dump_json(), ex=CACHE_TTL_SECONDS)
        except RedisError:
            logger.warning("Redis SET failed for %s", key, exc_info=True)