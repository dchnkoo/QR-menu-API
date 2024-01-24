from pydantic import BaseModel


class RestaurantRegister(BaseModel):
    token: str
    name: str
    address: str
    start_day: str = None
    end_day: str = None
    start_time: str = None
    end_time: str = None
    logo: str = None


class RestaurantUpdate(BaseModel):
    token: str
    name: str = None
    address: str = None
    start_day: str = None
    end_day: str = None
    start_time: str = None
    end_time: str = None
    logo: str = None