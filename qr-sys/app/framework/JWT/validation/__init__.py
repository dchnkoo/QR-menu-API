from fastapi import Request, HTTPException

from .. import jwt

from ....settings import logger


class JWTValidation:

    def __call__(self, request: Request):        
        try: token = request.cookies.get('token')
        except Exception as e:
            logger.error(f"Спроба взаємодії без дійсного JWT")
            raise HTTPException(status_code=403, detail="Відсутній JWT token")

        is_valid = jwt.check_token(token)

        if is_valid[0] is False:
       
            try: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
            except Exception as e: logger.error(f"JWT відсутній в JWTMetaData\n\nError: {e}")

            raise HTTPException(status_code=401, detail=is_valid[1])
        
        if request.method == "DELETE" and request.url.path.endswith("delete/session/user"):
            try: jwt.delete(token)
            except Exception as e:
                logger.error(f"Помилка під час видалення токену {token[-10:]}")
                raise HTTPException(status_code=500, detail="Невідома помилка")
            
            raise HTTPException(status_code=200, detail="Користувача видаленно з сессії")

        if request.method == "DELETE" and request.url.path.endswith("delete/user"):
            try: 
                return jwt.pop(token)
            except Exception as e:
                logger.error(f"Помилка під час видалення токену {token[-10:]}\n Error: {e}")
                raise HTTPException(status_code=500, detail="Невідома помилка")
            

        try: return jwt.get(token)
        except Exception: raise HTTPException(status_code=500, detail="Невідома помилка спробуйте знову згенерувати токен")