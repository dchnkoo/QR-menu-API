from pydantic import BaseModel, Field
from typing import Optional


class RestaurantRegister(BaseModel):
    name: str
    address: Optional[str] = Field(None, description="Адреса закладу")
    start_day: Optional[str] = Field(None, description="День початку роботи закладу")
    end_day: Optional[str] = Field(None, description="День закінчення роботи закладу")
    start_time: Optional[str] = Field(None, description="Година початку роботи закладу")
    end_time: Optional[str] = Field(None, description="День закінчення роботи закладу")
    logo: Optional[str] = Field(None, description="Логотип закладу. Повинен бути перетворений в base64 та декоований в utf-8")


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = Field(None, description="Адреса закладу")
    start_day: Optional[str] = Field(None, description="День початку роботи закладу")
    end_day: Optional[str] = Field(None, description="День закінчення роботи закладу")
    start_time: Optional[str] = Field(None, description="Година початку роботи закладу")
    end_time: Optional[str] = Field(None, description="День закінчення роботи закладу")
    logo: Optional[str] = Field(None, description="Логотип закладу. Повинен бути перетворений в base64 та декоований в utf-8")