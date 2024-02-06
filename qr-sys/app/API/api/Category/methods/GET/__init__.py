from ......framework import app, jwt_validation, logger, db, t

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Category import GetCategories
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant, categories, dishes,
                                 ingredients)
from ...tags.tags import CATEGORY


@app.get('/api/admin/get/categories', tags=[CATEGORY])
async def get_categories(hashf: str = Depends(jwt_validation)) -> (GetCategories | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час обробки транзакції'})


    try: category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                    to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': "Невідома помилка під час обробки запиту"})
    
    return JSONResponse(status_code=200, content={'categories': category})


@app.get("/api/admin/get-full-info/categories", tags=[CATEGORY])
async def get_full_info_categories(hashf: str = Depends(jwt_validation)):
    
    restaurant_ = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                           all_=False, to_dict=True)
    
    if restaurant_ is None:
        return JSONResponse(status_code=500, content={"msg": "Неможливо виконати запит через відсутність зарєстрованого закладу у користувача"})

    restaurant_ = t.parse_user_data(restaurant_)

    restaurant_id = restaurant_['id']
    
    category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                        to_dict=True)
    
    info = {"restaurant": restaurant_ | {"categories": category}}

    if category:
        dishes_data = await db.async_get_where(dishes, exp=dishes.c.restaurant_id == restaurant_id,
                                               to_dict=True)
        
        ingredients_data = await db.async_get_where(ingredients, exp=ingredients.c.restaurant_id == restaurant_id,
                                                    to_dict=True)
        
        for i in range(len(category)):
            category_id = category[i]["id"]
            category[i]["dishes"] = []
            
            for j in range(len(dishes_data)):
                category_dish_id = dishes_data[j]["category_id"]
                dishes_data[j]["ingredients"] = []

                if category_id == category_dish_id:
                    category[i]["dishes"].append(dishes_data[j])

                for l in range(len(ingredients_data)):

                    dish_id = dishes_data[j]["id"]
                    ingredients_id = ingredients_data[l]["dish_id"]

                    if dish_id == ingredients_id:
                        dishes_data[j]["ingredients"].append(ingredients_data[l])

    return JSONResponse(status_code=200, content=info)