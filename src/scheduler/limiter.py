from aiolimiter import AsyncLimiter

MAX_MESSAGES_PER_SECOND = 30
RATE_LIMITER = AsyncLimiter(MAX_MESSAGES_PER_SECOND, 1.0)
