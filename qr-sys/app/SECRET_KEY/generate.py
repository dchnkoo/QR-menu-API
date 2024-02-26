from app.settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_DB
import os

from random import randint
import argparse
import redis


env = os.environ

def set_secret():
    SECRET_KEY = "".join([chr(randint(33, 125)) for _ in range(70)])

    re = redis.Redis(
        password=env.get("REDIS_PASSWORD", REDIS_PASSWORD),
        host=env.get('REDIS_HOST', REDIS_HOST),
        port=env.get('REDIS_PORT', REDIS_PORT),
        decode_responses=True,
        db=int(env.get('REDIS_DB', REDIS_DB)) + 2,
    )

    re.set("SECRET_KEY", SECRET_KEY)

    print("KEY SET SUCCESFULY")

parser = argparse.ArgumentParser()
parser.add_argument("--set-secret", action=set_secret())