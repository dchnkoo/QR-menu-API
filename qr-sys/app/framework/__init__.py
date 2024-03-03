# Асинхрона модель взаємодії з базою данних
from ..database.db.models._async import async_db
db = async_db()

# Скупчення методів які не знаєш куди припихнути
from .trash_methods.trash import trash
t = trash()


# Обьєкт керування токенами
from .JWT import jwt


# Логер та сам додаток 
from ..settings import logger, app

# Обьєкт керування QR кодом (створення, видалення и т.д.)
from ..API.QR.object.qr import QR
qr = QR()

# Обьєкт який надсилає поштові листи взаємодія в парі з celery 
from .email.object import send_mail

# Обьєкт створення та перевірки кодів для відновлення паролю
# має обмеження по часу збереження в redis
from .recovery.password.object import recovery_codes
recovery = recovery_codes()