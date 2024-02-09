from pydantic import BaseModel


class RecoverySetCode(BaseModel):
    email: str

class Recovery(BaseModel):
    email: str
    code: str

class RecoveryPassword(BaseModel):
    email: str
    password: str
