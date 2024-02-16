from ...settings import REDIS_PORT, DEBUG, REDIS_HOST

import redis
import os


def get_redis_connection(db: int) -> redis.Redis:
    return redis.from_url(
        f"redis://{REDIS_HOST if DEBUG else os.environ.get('REDIS_HOST')}:{REDIS_PORT if DEBUG else os.environ.get('REDIS_PORT')}/{db}"
    )