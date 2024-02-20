from celery import Celery
import os

from ....settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, DEBUG


env = os.environ

D = REDIS_DB + 1 if DEBUG else int(env.get("REDIS_DB")) + 1
H = REDIS_HOST if DEBUG else env.get("REDIS_HOST")
P = REDIS_PORT if DEBUG else env.get("REDIS_PORT")
PASS = REDIS_PASSWORD if DEBUG else env.get("REDIS_PASSWORD")

celery = Celery("tasks", broker=f"redis://:{PASS}@{H}:{P}/{D}")