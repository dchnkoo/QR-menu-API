from pydantic import BaseModel


class Dish(BaseModel):
    img: str = ''
    name: str
    price: int
    weight: int
    comment: str = ''
    category_id: int


class DishAdd(BaseModel):
    data: Dish


class DishDelete(BaseModel):
    dish_id: int
    category_id: int