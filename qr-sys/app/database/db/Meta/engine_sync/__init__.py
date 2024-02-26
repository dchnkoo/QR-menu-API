from sqlalchemy import create_engine

from .....settings import DATABASE_SYNC
import os

# Ініціалізація синхроного підключення до БД
engine = create_engine(os.environ.get("DATABASE_URL_SYNC", DATABASE_SYNC))