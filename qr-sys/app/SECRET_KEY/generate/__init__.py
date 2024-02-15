from ...settings import REDIS_HOST, REDIS_PORT, REDIS_DB, DEBUG
import os

from random import randint
import argparse
import redis


def set_secret():
    SECRET_KEY = "".join([chr(randint(33, 125)) for _ in range(70)])

    re = redis.from_url(
        f"redis://{REDIS_HOST if DEBUG else os.environ.get('REDIS_HOST')}:{REDIS_PORT if DEBUG else os.environ.get('REDIS_PORT')}/{REDIS_DB + 2}"
    )

    re.set("SECRET_KEY", SECRET_KEY)


parser = argparse.ArgumentParser()
parser.add_argument("--set-secret", action=set_secret())