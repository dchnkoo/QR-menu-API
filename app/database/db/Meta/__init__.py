from app import settings

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine


# Визначаємо підключення до бази данних та базову модель
metadata = MetaData()

engine = create_async_engine(settings.DATABASE)