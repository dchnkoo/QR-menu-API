from pydantic import BaseModel
from typing import Union

from ..JWT import JWTliveTime


class LoginByToken(BaseModel):
    token: str

class LoginByLP(BaseModel):
    email: str
    password: str
    time: JWTliveTime

class Login(BaseModel):
    type: str = 'login'
    data: Union[LoginByLP, LoginByToken]