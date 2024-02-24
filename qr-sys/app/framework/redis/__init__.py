from ...settings import (REDIS_PORT, DEBUG, 
                         REDIS_HOST, REDIS_PASSWORD)

import redis
import os


env = os.environ

def get_redis_connection(db: int) -> redis.Redis:
    """Отримати підключення до redis"""
    return redis.Redis(
        password=REDIS_PASSWORD if DEBUG else env.get("REDIS_PASSWORD"),
        host=REDIS_HOST if DEBUG else env.get('REDIS_HOST'),
        port=REDIS_PORT if DEBUG else env.get('REDIS_PORT'),
        decode_responses=True,
        db=db,
    )