import redis
import os

from ...settings import REDIS_PORT, DEBUG, REDIS_HOST, REDIS_DB

re = redis.Redis(
    host=REDIS_HOST if DEBUG else os.environ.get("REDIS_HOST"),
    port=REDIS_PORT if DEBUG else int(os.environ.get("REDIS_PORT")),
    db=REDIS_DB if DEBUG else int(os.environ.get("REDIS_DB"))
)