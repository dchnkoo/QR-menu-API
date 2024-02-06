from pydantic import BaseModel


class Dish(BaseModel):
    img: str = ''
    name: str
    price: int
    weight: int
    comment: str = ''
    category_id: int
