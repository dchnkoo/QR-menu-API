from pydantic import BaseModel
from ..Dishes import Dish


class Ingredient(BaseModel):
    id: int
    ingredient: str
    restaurant_id: int


class IngredientResponse(BaseModel):
    status: int
    ingredient: Ingredient
    dish: Dish