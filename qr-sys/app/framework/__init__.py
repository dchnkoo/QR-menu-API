from ..database.db.models._async import async_db
from .trash_methods.trash import trash

from .JWT import jwt
from .JWT.validation import JWTValidation

from ..settings import logger, app

from ..API.QR.object.qr import QR

# JWT
jwt_validation = JWTValidation()

# Взаємодія з базою данних
db = async_db()

# other methods
t = trash()

# QR-code 
qr = QR()