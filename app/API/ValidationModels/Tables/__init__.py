from pydantic import BaseModel
from typing import Union


class CreateTable(BaseModel):
    token: str
    table_number: int = 1

class DelDataValidationA(BaseModel):
    type: str

class DelDataValidationB(BaseModel):
    type: str
    table_number: int

class DeleteTable(BaseModel):
    token: str
    data: Union[DelDataValidationB, 
                DelDataValidationA]
