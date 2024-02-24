from sqlalchemy import create_engine

from .....settings import DATABASE_SYNC, DEBUG
import os

# Ініціалізація синхроного підключення до БД
engine = create_engine(DATABASE_SYNC if DEBUG else os.environ.get("DATABASE_URL_SYNC"))