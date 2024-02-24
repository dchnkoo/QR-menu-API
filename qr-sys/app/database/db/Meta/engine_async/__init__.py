from app.settings import DATABASE, DEBUG
import os

from sqlalchemy.ext.asyncio import create_async_engine

# Ініціалізація асинхроного підключення до БД
engine = create_async_engine(DATABASE if DEBUG else os.environ.get("DATABASE_URL"))