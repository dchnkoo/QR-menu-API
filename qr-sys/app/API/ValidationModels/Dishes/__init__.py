from pydantic import BaseModel, Field, validator
from fastapi.exceptions import HTTPException

from ....settings import DISHES_IMG
from ....framework import t



class Dish(BaseModel):
    img: str = Field(None, description=f"Картинка для блюда повинна бути в base64 str та розміром {DISHES_IMG}x{DISHES_IMG} (необов'язковий)")
    name: str
    price: int
    weight: int
    comment: str = Field(None, description="Коментар для блюда (необов'язковий)")
    category_id: int

    @validator("img")
    def check_img(cls, value):
        if value:
            status, code, msg = t.check_images_size(value, DISHES_IMG, DISHES_IMG)

            if status is False:
                raise HTTPException(status_code=code, detail=msg)
            
        return value
