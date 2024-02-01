import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from ..MetaData.jwt_metadata import JWTMetaData 

import datetime

from ....settings import SECRET_KEY, logger


class JWT:

    def __init__(self) -> None:
        self._token = JWTMetaData()

    def get_playload(self, id: int, udata: str, **exp_time) -> dict:
        return {
            'user_id': id,
            'username': udata,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(**exp_time)
        }

    
    def get_token(self, **playload) -> str:
        token = jwt.encode(playload, 
                           SECRET_KEY,
                           algorithm='HS256')
        
        logger.info(f"create JWT token for {playload['username']} exp time to {playload['exp']}")
        return token
    

    def check_token(self, token: jwt) -> list[bool, dict | str, str]:
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


    def save_token(self, token: str, hashf: str) -> None:
        self._token[token] = hashf

    def delete_token(self, token) -> None:
        del self._token[token]

    def get_user_hash(self, token: str) -> str:
        return self._token[token]