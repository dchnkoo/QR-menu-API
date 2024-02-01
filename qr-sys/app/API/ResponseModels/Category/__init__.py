from pydantic import BaseModel
from typing import List


class CategoryTable(BaseModel):
    id: int
    category: str
    color: str
    restaurant_id: int

class CategoryAddResponse(BaseModel):
    status: int
    category: CategoryTable


class GetCategories(BaseModel):
    status: int
    categories: List[CategoryTable]