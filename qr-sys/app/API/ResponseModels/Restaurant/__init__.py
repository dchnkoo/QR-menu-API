from pydantic import BaseModel


class RestaurantData(BaseModel):
    id: int
    name: str
    address: str = None
    start_day: str = None
    end_day: str = None
    start_time: str = None
    end_time: str = None


class RestaurantResponseSucces(BaseModel):
    restaurant_data: RestaurantData