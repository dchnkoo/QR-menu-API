from .....ResponseModels.Register import RegisterResponseFail
from ......framework import app, jwt_validation, db, logger
from ......database.tables import dishes, restaurant
from .....ValidationModels.Dishes import Dish
from .....tags import DISHES

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.post('/api/admin/add/dish', tags=[DISHES])
async def add_dish(data: Dish, hashf: str = Depends(jwt_validation)) -> Dish:

    insert_data = data.model_dump()

    restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                             all_=False, to_dict=True)
    
    insert_data = insert_data | {"restaurant_id": restaurant_id.get("id")}

    try: new_dish = await db.async_insert_data(dishes, to_dict=True, **insert_data)
    except Exception as e:
        logger.error(f"Помилка при додавані страви\n\nСессія: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час виконання')

    return JSONResponse(status_code=200, content=new_dish)    