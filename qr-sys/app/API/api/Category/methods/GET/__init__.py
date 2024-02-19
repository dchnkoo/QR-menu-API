from ......framework import app, jwt_validation, logger, db, t

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Category import GetCategories
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant, categories, dishes,
                                 ingredients)
from .....tags import CATEGORY


@app.get('/api/admin/get/categories', tags=[CATEGORY])
async def get_categories(hashf: str = Depends(jwt_validation)) -> (GetCategories | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки транзакції')


    try: category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                    to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки запиту")
    
    return JSONResponse(status_code=200, content={'categories': category})


@app.get("/api/admin/get-full-info/categories", tags=[CATEGORY])
async def get_full_info_categories(hashf: str = Depends(jwt_validation)):
    
    restaurant_ = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                           all_=False, to_dict=True)
    
    if restaurant_ is None:
        raise HTTPException(status_code=500, detail="Неможливо виконати запит через відсутність зарєстрованого закладу у користувача")

    restaurant_ = t.parse_user_data(restaurant_)

    restaurant_id = restaurant_['id']
    
    category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                        to_dict=True)

    if category:
        dishes_data = await db.async_get_where(dishes, exp=dishes.c.restaurant_id == restaurant_id,
                                               to_dict=True)
        
        ingredients_data = await db.async_get_where(ingredients, exp=ingredients.c.restaurant_id == restaurant_id,
                                                    to_dict=True)

        category = [
            {**i, "dishes": [

                {**j, "ingredients": [
            
                    l for l in ingredients_data if j.get("id") == l.get("dish_id")
            
                ]} for j in dishes_data if j.get("category_id") == i.get("id")
            
            ]} for i in category
        ]

    info = {"restaurant": restaurant_ | {"categories": category}}
    
    return JSONResponse(status_code=200, content=info)