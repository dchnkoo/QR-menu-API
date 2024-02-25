from pydantic import BaseModel, Field, validator
from typing import Tuple
from enum import Enum

from ....settings import TABLES_PER_TRANSACTION


class CreateTable(BaseModel):
    table_number: int = Field(1, ge=1, le=TABLES_PER_TRANSACTION, description=f"За одну транзацію можливо згенерувати максимум {TABLES_PER_TRANSACTION} столів")
    background: Tuple[int, int, int] = Field(default=(255, 255, 255),
                                            description="RGB value",
                                            min_length=3, max_length=3)
    fill_lines: Tuple[int, int, int] = Field(default=(0, 0, 0),
                                            description="RGB value",
                                            min_length=3, max_length=3)
    logo: bool = False


    @validator("background", "fill_lines")
    def check_rgb_value(cls, value):
        if not all(0 <= num <= 255 for num in value):
            raise ValueError("RGB values must be beetwen 0 and 255")
        return value


class DeleteType(str, Enum):
    all = "all"
    table = "table"