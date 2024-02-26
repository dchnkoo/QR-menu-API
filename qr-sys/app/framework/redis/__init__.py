from ...settings import (REDIS_PORT, REDIS_HOST, REDIS_PASSWORD)

import redis
import os


env = os.environ

def get_redis_connection(db: int) -> redis.Redis:
    """Отримати підключення до redis"""
    return redis.Redis(
        password=env.get("REDIS_PASSWORD", REDIS_PASSWORD),
        host=env.get('REDIS_HOST', REDIS_HOST),
        port=env.get('REDIS_PORT', REDIS_PORT),
        decode_responses=True,
        db=db,
    )