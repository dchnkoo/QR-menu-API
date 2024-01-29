from pydantic import BaseModel
   

class IngredientScheme(BaseModel):
    ingredient: str
    dish_id: int


class DeleteIngredient(BaseModel):
    ingredient_id: int
    dish_id: int