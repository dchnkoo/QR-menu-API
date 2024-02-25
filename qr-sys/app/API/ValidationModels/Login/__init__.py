from pydantic import BaseModel
from ..JWT import JWTliveTime


class LoginByLP(BaseModel):
    email: str
    password: str
    time: JWTliveTime