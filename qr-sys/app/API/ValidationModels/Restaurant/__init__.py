from pydantic import BaseModel


class RestaurantRegister(BaseModel):
    name: str
    address: str
    start_day: str = None
    end_day: str = None
    start_time: str = None
    end_time: str = None
    logo: str = None


class RestaurantUpdate(BaseModel):
    name: str = None
    address: str = None
    start_day: str = None
    end_day: str = None
    start_time: str = None
    end_time: str = None
    logo: str = None