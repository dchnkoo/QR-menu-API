from fastapi import FastAPI

from ..database.db.db_model import DB
from .trash_methods.trash import trash

# ініціалізуємо апі додаток
app = FastAPI(
    title='QR-menu System'
)

# Взаємодія з базою данних
db = DB()

t = trash()