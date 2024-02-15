from pydantic import BaseModel, Field


class RecoverySetCode(BaseModel):
    email: str

class Recovery(BaseModel):
    email: str
    code: str

class RecoveryPassword(BaseModel):
    id: int = Field(..., 
                    description="id користувача яке отримали після успішної перевірки коду")
    password: str = Field(..., description="Новий пароль для користувача")
