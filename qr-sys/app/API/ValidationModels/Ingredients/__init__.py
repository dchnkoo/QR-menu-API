from pydantic import BaseModel
   

class IngredientScheme(BaseModel):
    ingredient: str
    dish_id: int