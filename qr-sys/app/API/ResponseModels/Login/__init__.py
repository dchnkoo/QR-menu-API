from pydantic import BaseModel
from ..Register import RegisterUserData



class SuccesLogin(BaseModel):
    user_data: RegisterUserData