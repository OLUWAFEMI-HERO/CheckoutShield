from redis.exceptions import RedisError


class VelocityService:

    def __init__(self, time_window_seconds: int = 60, max_attempts: int = 5):
        self.time_window = time_window_seconds
        self.max_attempts = max_attempts
        # Stores timestamps of requests: {"user@email.com": [timestamp1, timestamp2]}
        self._history = defaultdict(list)

    def check_and_record(self, identifier: str) -> bool:
        now = time.time()
        # Clean up old records outside the time window
        self._history[identifier] = [
            t for t in self._history[identifier] 
            if now - t < self.time_window
        ]
        
        # Check if they exceeded the limit
        if len(self._history[identifier]) >= self.max_attempts:
            return False # Velocity limit breached
            
        # Record the new attempt
        self._history[identifier].append(now)
        return True

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

# Singleton instance
velocity_engine = VelocityTracker()