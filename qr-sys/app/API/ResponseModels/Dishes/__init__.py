from pydantic import BaseModel
from typing import List

from ...ValidationModels.Dishes import Dish


class DishResponse(Dish):
    id: int
    
class DishResponseList(BaseModel):
    data: List[Dish]