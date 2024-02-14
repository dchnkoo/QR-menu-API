from pydantic import BaseModel, Field, validator
from typing import Tuple


class CreateTable(BaseModel):
    table_number: int = 1
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

class DelDataValidationA(BaseModel):
    type: str

class DelDataValidationB(BaseModel):
    type: str
    table_number: int