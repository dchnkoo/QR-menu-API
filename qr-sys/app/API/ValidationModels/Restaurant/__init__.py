from pydantic import BaseModel, Field, validator

from ....settings import MAX_WIDTH, MAX_HEIGHT
from fastapi.exceptions import HTTPException
from ....framework import t

from typing import Optional


class RestaurantRegister(BaseModel):
    name: str
    address: Optional[str] = Field(None, description="Адреса закладу")
    start_day: Optional[str] = Field(None, description="День початку роботи закладу")
    end_day: Optional[str] = Field(None, description="День закінчення роботи закладу")
    start_time: Optional[str] = Field(None, description="Година початку роботи закладу")
    end_time: Optional[str] = Field(None, description="День закінчення роботи закладу")
    logo: Optional[str] = Field(None, description="Логотип закладу. Повинен бути перетворений в base64 та декоований в utf-8")


    @validator("logo")
    def check_logo(cls, value):
        if value is not None:
            status, code, msg = t.check_images_size(value, MAX_WIDTH, MAX_HEIGHT)

            if status is False:
                raise HTTPException(status_code=code, detail=msg)
            
        return value


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = Field(None, description="Адреса закладу")
    start_day: Optional[str] = Field(None, description="День початку роботи закладу")
    end_day: Optional[str] = Field(None, description="День закінчення роботи закладу")
    start_time: Optional[str] = Field(None, description="Година початку роботи закладу")
    end_time: Optional[str] = Field(None, description="День закінчення роботи закладу")
    logo: Optional[str] = Field(None, description="Логотип закладу. Повинен бути перетворений в base64 та декоований в utf-8")

    @validator("logo")
    def check_logo(cls, value):
        if value is not None:
            status, code, msg = t.check_images_size(value, MAX_WIDTH, MAX_HEIGHT)

            if status is False:
                raise HTTPException(status_code=code, detail=msg)
            
        return value