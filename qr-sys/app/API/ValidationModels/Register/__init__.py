from pydantic import BaseModel
from ..JWT import JWTliveTime


class RegisterUser(BaseModel):
    email: str 
    password: str 
    time: JWTliveTime