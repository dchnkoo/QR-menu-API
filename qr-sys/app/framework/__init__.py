from ..database.db.models._async import async_db
db = async_db()


from .trash_methods.trash import trash
t = trash()



from .JWT import jwt
from .JWT.validation import JWTValidation
jwt_validation = JWTValidation()



from ..settings import logger, app


from ..API.QR.object.qr import QR
qr = QR()


from .email.object import email
send_mail = email()


from .recovery.password.object import recovery_codes
recovery = recovery_codes()