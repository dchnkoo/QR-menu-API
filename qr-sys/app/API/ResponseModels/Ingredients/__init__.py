from pydantic import BaseModel
from typing import List


class Ingredient(BaseModel):
    id: int
    ingredient: str
    dish_id: int
    restaurant_id: int

class IngredientGetResponse(BaseModel):
    data: List[Ingredient]
