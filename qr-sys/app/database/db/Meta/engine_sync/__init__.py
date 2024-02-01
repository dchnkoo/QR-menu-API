from sqlalchemy import create_engine
from .....settings import DATABASE_SYNC


engine = create_engine(DATABASE_SYNC)