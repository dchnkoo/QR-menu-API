from pydantic import BaseModel
from typing import Union


class CategorySet(BaseModel):
    token: str
    category: str
    color: str


class CategoryAll(BaseModel):
    type: str = 'all'

class CategoryId(BaseModel):
    type: str = "category"
    category_id: int 

class CategoryDelete(BaseModel):
    token: str
    delete: Union[CategoryId, CategoryAll]