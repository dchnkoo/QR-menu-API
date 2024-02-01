from pydantic import BaseModel
from typing import Union


class CategorySet(BaseModel):
    category: str
    color: str


class CategoryAll(BaseModel):
    type: str = 'all'

class CategoryId(BaseModel):
    type: str = "category"
    category_id: int 

class CategoryDelete(BaseModel):
    delete: Union[CategoryId, CategoryAll]