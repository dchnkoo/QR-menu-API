from ..database.db.models.db_model import DB
from .trash_methods.trash import trash

from .JWT.token.auth import JWT
from .JWT.validation import JWTValidation

from ..settings import logger, app

from ..API.QR.object.qr import QR

# JWT
jwt_validation = JWTValidation()
jwt = JWT()

# Взаємодія з базою данних
db = DB()

# other methods
t = trash()

# QR-code 
qr = QR()