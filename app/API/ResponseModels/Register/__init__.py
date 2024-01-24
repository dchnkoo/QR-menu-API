from pydantic import BaseModel


class RegisterUserData(BaseModel):
    id: int
    email: str

class RegisterResponseSucces(BaseModel):
    status: int
    token: str
    user_data: RegisterUserData

class RegisterResponseFail(BaseModel):
    status: int
    msg: str