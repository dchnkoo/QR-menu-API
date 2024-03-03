from ......framework import app, jwt, t, db, logger
from ......database.tables import restaurant

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Restaurant import RestaurantUpdate, RestaurantDataDelete
from .....ResponseModels.Restaurant import RestaurantResponseSucces

from .....tags import RESTAURANT


@app.patch('/api/admin/update/restaurant', tags=[RESTAURANT])
async def restaurant_data_update(data: RestaurantUpdate, hashf: str = Depends(jwt)) -> RestaurantResponseSucces:

    try: new_data = await db.async_update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                **t.parse_user_data(data.model_dump()), to_dict=True)
    except Exception as e:
        logger.error(f"Помилка при оновленні даннних закладу\n\nhashf: {hashf}\n\n Error: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час виконання операції')
    
    if new_data is None:
        raise HTTPException(status_code=400, detail="Відсутній заклад")

    return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(new_data)})

@app.patch("/api/admin/delete/data", tags=[RESTAURANT])
async def delete_restaurant_data(data: RestaurantDataDelete, hashf: str = Depends(jwt)) -> RestaurantResponseSucces:
    
    """
    <h1>Якщо ключ має значення true тоді це поле буде видаленно з БД</h1>
    """

    # Якщо поле true тоді додаємо його до словника та змінюємо значення на None
    columns = {k: None for k, v in data.model_dump().items() if v}

    if not columns.keys():
        raise HTTPException(status_code=400, detail="Не вибрано колонок для видалення")

    try: update_data = await db.async_update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                                  **columns, to_dict=True)
    except Exception as e: 
        logger.error(f"Помилка під час видалення данних з колонок.\n\nhashf: {hashf}\nError: {e}")
        raise HTTPException(status_code=400, detail="Відстуній заклад для редагування.")
    
    if update_data is None:
        raise HTTPException(status_code=400, detail="Невідома помилка")

    return JSONResponse(status_code=200, content={"restaurant_data": t.parse_user_data(update_data)})