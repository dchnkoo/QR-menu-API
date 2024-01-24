from fastapi import FastAPI

from ..database.db.db_model import DB
from .trash_methods.trash import trash

from .JWT.token.auth import JWT

from ..settings import logger

from ..API.QR.object.qr import QR

# ініціалізуємо апі додаток
app = FastAPI(
    title='QR-menu System'
)

# Взаємодія з базою данних
db = DB()

t = trash()

jwt = JWT()

qr = QR()