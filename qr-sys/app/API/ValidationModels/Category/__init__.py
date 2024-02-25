from pydantic import BaseModel, Field, validator
from enum import Enum

from random import randint
from typing import Tuple


class CategorySet(BaseModel):
    category: str
    color: Tuple[int, int, int] = Field(default_factory=lambda: [randint(170, 255) for _ in range(3)],
                            description="RGB value",
                            min_length=3, max_length=3)

    @validator("color")
    def check_rgb_value(cls, value):
        if not all(0 <= num <= 255 for num in value):
            raise ValueError("RGB values must be beetwen 0 and 255")
        return value

class CategoryDelType(str, Enum):
    all = "all"
    category = "category"