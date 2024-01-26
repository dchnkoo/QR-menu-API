from pydantic import BaseModel


class Dish(BaseModel):
    id: int
    img: str = ''
    name: str
    price: int
    weight: int
    comment: str = ''
    category_id: int

class DishResponse(BaseModel):
    status: int
    token: str
    dish: Dish