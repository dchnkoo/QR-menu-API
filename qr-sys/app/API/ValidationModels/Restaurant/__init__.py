from pydantic import BaseModel
from typing import Optional


class RestaurantRegister(BaseModel):
    name: str
    address: Optional[str] = None
    start_day: Optional[str] = None
    end_day: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    logo: Optional[str] = None


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    start_day: Optional[str] = None
    end_day: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    logo: Optional[str] = None