from redis.exceptions import RedisError


class VelocityService:

    def __init__(self, redis):
        self.redis = redis

    async def record_checkout(
        self,
        merchant_id: str,
        customer_id: str,
    ) -> int:

        key = (
            f"velocity:"
            f"{merchant_id}:"
            f"customer:{customer_id}"
        )

        try:
            count = await self.redis.incr(key)

            if count == 1:
                await self.redis.expire(key, 60)

            return count

        except RedisError:
            # Do not fail checkout because the
            # optional velocity signal is unavailable.
            return 0