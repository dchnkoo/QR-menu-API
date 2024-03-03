from ...settings import COOKIE_KEY

def get_dishes(category_id: int) -> list[dict]:
    dishes = [{
                "img": "",
                "name": "Dish 1",
                "price": 0,
                "weight": 0,
                "comment": "",
                "category_id": category_id
            }, {
                "img": "",
                "name": "Dish 2",
                "price": 0,
                "weight": 0,
                "comment": "",
                "category_id": category_id
            }]
    
    return dishes

async def add_dish(client, token: str, dish: dict):
    cookie = {COOKIE_KEY: token}

    request = await client.post("/api/admin/add/dish", cookies=cookie, json=dish)

    return request.status_code, request.json()

async def delete_dish(client, token: str, **kwargs):
    cookie = {COOKIE_KEY: token}

    args = "".join([f"{k}={v}&" for k, v in kwargs.items()])[:-1]

    request = await client.delete(f"/api/admin/delete/dish?{args}", cookies=cookie)

    return request.status_code, request.json()