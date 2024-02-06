
def get_ingredient(dish_id: int):
    return [{"ingredient": "Крем", "dish_id": dish_id},
            {"ingredient": "Картопля", "dish_id": dish_id},
            {"ingredient": "Сало", "dish_id": dish_id}]

async def add_ingredient(client, token: str, data: dict):
    cookie = {"token": token}

    request = await client.post("/api/admin/add/ingredient", 
                          cookies=cookie, json=data)
    
    return request.status_code, request.json()

async def delete_ingredient(client, token: str, dish_id: int, ingredient_id: int):
    cookie = {"token": token}

    request = await client.delete(f"/api/admin/delete/ingredients?dish_id={dish_id}&ingredient_id={ingredient_id}", 
                          cookies=cookie)
    
    return request.status_code, request.json()