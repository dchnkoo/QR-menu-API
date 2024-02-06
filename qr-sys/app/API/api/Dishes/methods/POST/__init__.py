from ......framework import app, jwt_validation, db, logger

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Dishes import Dish
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import dishes, restaurant
from ...tags.tags import DISHES


@app.post('/api/admin/add/dish', tags=[DISHES])
async def add_dish(data: Dish, hashf: str = Depends(jwt_validation)) -> (Dish | RegisterResponseFail):

    insert_data = data.model_dump()

    restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                             all_=False)
    
    insert_data = insert_data | {"restaurant_id": restaurant_id[0]}

    try: new_dish = await db.async_insert_data(dishes, **insert_data)
    except Exception as e:
        logger.error(f"Помилка при додавані страви\n\nСессія: {hashf}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час виконання'})

    return JSONResponse(status_code=200, content=new_dish._asdict())    