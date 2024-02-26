from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from ..MetaData.jwt_metadata import JWTMetaData 
import jwt

from ...redis import get_redis_connection
from ....settings import REDIS_DB, logger
import datetime, os


SECRET_KEY = get_redis_connection(int(os.environ.get("REDIS_DB", REDIS_DB)) + 2).get("SECRET_KEY")


class JWT(JWTMetaData):

    def get_playload(self, id: int, udata: str, **exp_time):
        """
        Створення обьєкту для генерування токену, також повертає 
        дату до котрої він буде дійсний в UTC форматі та кількість секунд
        до кінця його життя
        """
        exp_utc = datetime.datetime.utcnow() + datetime.timedelta(**exp_time)
        return {
            'user_id': id,
            'username': udata,
            'exp': exp_utc
        }, exp_utc.strftime("%a, %d-%b-%Y %T GMT"), int((exp_utc - datetime.datetime.utcnow()).total_seconds())

    
    def get_token(self, **playload) -> str:
        """
        Створити токен
        """
        token = jwt.encode(playload, 
                           SECRET_KEY,
                           algorithm='HS256')
        
        logger.info(f"create JWT token for {playload['username']} exp time to {playload['exp']}")
        return token

    def check_token(self, token: jwt) -> list[bool, dict | str, str]:
        """Перевірка дісйність токену"""
        try:
            check = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            logger.info(f"token {token[:10]} is valid")
            return [True, check, token]
        
        except ExpiredSignatureError:
            logger.error(f"Token {token[:10]} overdue. You need to update token.")
            return [False, 'Токен прострочений. Вам потрібно оновити токен.', token]

        except InvalidTokenError:
            logger.error(f"Token is invalid.")
            return [False, 'Недійсний токен. Перевірте ваш секретний ключ та токен.', token]

        except Exception as e:
            logger.error(f"Відсутній токен\n\nError: {e}")
            return [False, 'Відсутній токен']