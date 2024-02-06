from pydantic import BaseModel
from typing import List


class Dish(BaseModel):
    id: int
    img: str = ''
    name: str
    price: int
    weight: int
    comment: str = ''
    category_id: int

class DishResponseList(BaseModel):
    data: List[Dish]