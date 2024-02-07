
def get_restaurant() -> dict:
    return {"name": "PizzaDay"}


def get_restaurant_update() -> dict:
    return {"address": "st. Example, 202", "start_day": "Monday", "end_day": "Friday", "start_time": "9:00", "end_time": "21:00"}

async def delete_resturant(client, setup_user: str, cookies: bool = True) -> tuple:
    cookie = {"token": setup_user}

    request = await client.delete('/api/admin/delete/restaurant', cookies=cookie if cookies else None)

    return request.status_code, request.json()

async def register_restaurant(client, data: dict, token: str, cookies: bool = True):
    cookie = {"token": token}
    
    request = await client.post('/api/admin/add/restaurant',
                          cookies=cookie if cookies else None, json=data)
    
    return request.status_code, request.json()