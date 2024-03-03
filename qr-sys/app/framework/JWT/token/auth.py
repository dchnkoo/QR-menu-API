from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from ..MetaData.jwt_metadata import JWTMetaData 
from fastapi import Request, HTTPException
import jwt

from ....settings import REDIS_DB, logger, COOKIE_KEY
from ...redis import get_redis_connection
import datetime, os


SECRET_KEY = get_redis_connection(int(os.environ.get("REDIS_DB", REDIS_DB)) + 2).get("SECRET_KEY")


class JWT:

    def __init__(self) -> None:
        self.object = JWTMetaData()

    @staticmethod
    def cookie_params(token, date: datetime.datetime):
        return {"key": COOKIE_KEY, "value": token, "expires": date,
                                     "secure": True, "samesite": "none", "path": '/'}


    def get_playload(self, id: int, udata: str, **exp_time):
        """
        Створення обьєкту для генерування токену, також повертає 
        дату до котрої він буде дійсний в UTC форматі та кількість секунд
        до кінця його життя
        """
        exp_utc: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(**exp_time)
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
        
    # VALIDATION
    def __call__(self, request: Request):     
        try: token = request.cookies.get(COOKIE_KEY)
        except Exception as e:
            logger.error(f"Спроба взаємодії без дійсного JWT")
            raise HTTPException(status_code=403, detail="Відсутній JWT token")

        is_valid = self.check_token(token)

        if is_valid[0] is False:
       
            try: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
            except Exception as e: logger.error(f"JWT відсутній в JWTMetaData\n\nError: {e}")

            raise HTTPException(status_code=401, detail=is_valid[1])
        
        req_path = request.url.path
        if request.method == "DELETE" and (req_path.endswith("delete/session/user") or req_path.endswith("delete/user")):
            try: 
                return self.object.pop(token)
            except Exception as e:
                logger.error(f"Помилка під час видалення токену {token[-10:]}\nError: {e}")
                raise HTTPException(status_code=500, detail="Невідома помилка")
            

        try: return self.object.get(token)
        except Exception: raise HTTPException(status_code=500, detail="Невідома помилка спробуйте знову згенерувати токен")