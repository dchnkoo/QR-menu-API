from pydantic import BaseModel, Field, validator

from ....database.db.models.sync import sync_db
from ....database.tables import authefication
from ....framework import logger

from fastapi.exceptions import HTTPException


class ValidationEmail(BaseModel):
    email: str

    @validator("email")
    def check_user(cls, value):
        db = sync_db()
        
        try: find_user = db.get_where(authefication, exp=authefication.c.email == value,
                                              all_=False, to_dict=True)
        except Exception as e:
            logger.error(f"Помилка під час отримання емейлу для відновлення паролю.\n\nEmail: {value}\nError: {e}")
            raise HTTPException(status_code=400, detail="Помилка під час пошуку користувача")
        
        if find_user is None:
            raise HTTPException(status_code=400, detail="Користувч відстуній в системі")

        if issubclass(cls, Recovery):
            return value, find_user.get("id")

        return value


class RecoverySetCode(ValidationEmail):
    ...

class Recovery(ValidationEmail):
    code: str


class RecoveryPassword(BaseModel):
    id: int = Field(..., 
                    description="id користувача яке отримали після успішної перевірки коду")
    password: str = Field(..., description="Новий пароль для користувача")


    @validator("id")
    def check_user(cls, value):
        db = sync_db()
        
        try: find_user = db.get_where(authefication, exp=authefication.c.id == value,
                                              all_=False, to_dict=True)
        except Exception as e:
            logger.error(f"Помилка під час отримання емейлу для відновлення паролю.\n\nEmail: {value}\nError: {e}")
            raise HTTPException(status_code=400, detail="Помилка під час пошуку користувача")
        
        if find_user is None:
            raise HTTPException(status_code=400, detail="Користувч відстуній в системі")

        return value