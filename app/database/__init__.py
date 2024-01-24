from app import settings

import logging
from sqlalchemy import create_engine, MetaData


# Визначаємо підключення до бази данних та базову модель
metadata = MetaData()

engine = create_engine(settings.DATABASE, echo=True)