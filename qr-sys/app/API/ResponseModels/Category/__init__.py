from pydantic import BaseModel
from typing import List, Tuple


class CategoryTable(BaseModel):
    id: int
    category: str
    color: Tuple[int, int, int]
    restaurant_id: int


class GetCategories(BaseModel):
    status: int
    categories: List[CategoryTable]