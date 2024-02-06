from pydantic import BaseModel


class RegisterUserData(BaseModel):
    id: int
    email: str

class RegisterResponseSucces(BaseModel):
    token: str
    user_data: RegisterUserData

class RegisterResponseFail(BaseModel):
    msg: str