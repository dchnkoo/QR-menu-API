from pydantic import BaseModel


class Dish(BaseModel):
    img: str = ''
    name: str
    price: int
    weight: int
    comment: str = ''
    category_id: int


class DishAdd(BaseModel):
    token: str
    data: Dish


class DishDelete(BaseModel):
    token: str
    dish_id: int
    category_id: int