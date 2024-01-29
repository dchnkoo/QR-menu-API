from pydantic import BaseModel
from ..Register import RegisterUserData


class SuccesLogin(BaseModel):
    status: int
    user_data: RegisterUserData