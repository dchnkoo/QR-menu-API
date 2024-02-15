from pydantic import BaseModel
from enum import Enum


class JWTTimeUnit(str, Enum):
    minutes = "minutes"
    hours = "hours"
    days = "days"
    weeks = "weeks"


class JWTliveTime(BaseModel):
    type: JWTTimeUnit = "days"
    number: float = 1.0