from app.settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_DB, DEBUG
import os

from random import randint
import argparse
import redis


env = os.environ

def set_secret():
    SECRET_KEY = "".join([chr(randint(33, 125)) for _ in range(70)])

    re = redis.Redis(
        password=REDIS_PASSWORD if DEBUG else env.get("REDIS_PASSWORD"),
        host=REDIS_HOST if DEBUG else env.get('REDIS_HOST'),
        port=REDIS_PORT if DEBUG else env.get('REDIS_PORT'),
        decode_responses=True,
        db=REDIS_DB + 2 if DEBUG else int(env.get('REDIS_DB')) + 2,
    )

    re.set("SECRET_KEY", SECRET_KEY)


parser = argparse.ArgumentParser()
parser.add_argument("--set-secret", action=set_secret())