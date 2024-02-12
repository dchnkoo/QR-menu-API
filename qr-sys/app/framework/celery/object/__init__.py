from celery import Celery
import os

from ....settings import REDIS_DB, REDIS_HOST, REDIS_PORT, DEBUG


D = REDIS_DB + 1 if DEBUG else int(os.environ.get("REDIS_DB")) + 1
H = REDIS_HOST if DEBUG else os.environ.get("REDIS_HOST")
P = REDIS_PORT if DEBUG else os.environ.get("REDIS_PORT")

celery = Celery("tasks", broker=f"redis://{H}:{P}/{D}")