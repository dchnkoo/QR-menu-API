from ..database.db.models.async_model import DB
from .trash_methods.trash import trash

from .JWT import jwt
from .JWT.validation import JWTValidation

from ..settings import logger, app

from ..API.QR.object.qr import QR

# JWT
jwt_validation = JWTValidation()

# Взаємодія з базою данних
db = DB()

# other methods
t = trash()

# QR-code 
qr = QR()