from pydantic import BaseModel


class RegisterUserData(BaseModel):
    id: int
    email: str


class RegisterResponseFail(BaseModel):
    msg: str