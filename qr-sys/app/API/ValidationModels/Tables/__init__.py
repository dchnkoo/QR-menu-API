from pydantic import BaseModel
from typing import Union


class CreateTable(BaseModel):
    table_number: int = 1

class DelDataValidationA(BaseModel):
    type: str

class DelDataValidationB(BaseModel):
    type: str
    table_number: int

    
