from app.settings import DATABASE
import os

from sqlalchemy.ext.asyncio import create_async_engine

# Ініціалізація асинхроного підключення до БД
engine = create_async_engine(os.environ.get("DATABASE_URL", DATABASE))