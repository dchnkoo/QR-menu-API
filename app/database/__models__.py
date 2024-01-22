from . import tables
import sqlalchemy

# Отримуємо список таблиць в базі данних
tables_names = [i for i, v in vars(tables).items() if isinstance(v, sqlalchemy.sql.schema.Table)]