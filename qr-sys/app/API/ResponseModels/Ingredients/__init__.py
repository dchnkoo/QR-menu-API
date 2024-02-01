from pydantic import BaseModel
from typing import List


class Ingredient(BaseModel):
    id: int
    ingredient: str
    dish_id: int
    restaurant_id: int


class IngredientResponse(BaseModel):
    status: int
    ingredient: Ingredient

class IngredientGetResponse(BaseModel):
    status: int
    data: List[Ingredient]
