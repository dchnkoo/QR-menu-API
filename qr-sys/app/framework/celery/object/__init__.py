from celery import Celery
import os

from ....settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


env = os.environ

D = int(env.get("REDIS_DB", REDIS_DB)) + 1
H = env.get("REDIS_HOST", REDIS_HOST)
P = env.get("REDIS_PORT", REDIS_PORT)
PASS = env.get("REDIS_PASSWORD", REDIS_PASSWORD)

celery = Celery("tasks", broker=f"redis://:{PASS}@{H}:{P}/{D}", broker_connection_retry_on_startup=True)