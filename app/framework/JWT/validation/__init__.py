from ..token.auth import JWT
from fastapi import Request, HTTPException

from ....settings import logger


class JWTValidation:

    def __init__(self) -> None:
        self.jwt = JWT()

    def __call__(self, request: Request):        

        try: token = request.cookies.get('token')
        except Exception as e:
            logger.error(f"Спроба взаємодії без дійсного JWT")
            raise HTTPException(status_code=403, detail="Відсутній JWT token")

        is_valid = self.jwt.check_token(token)

        if not is_valid[0]:
            
            try: self.jwt.delete_token(token) 
            except: 
                try: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
                except Exception as e: logger.error(f"JWT відсутній в JWTMetaData\n\nError: {e}")

            raise HTTPException(status_code=403, detail=is_valid[1])
        
        return token