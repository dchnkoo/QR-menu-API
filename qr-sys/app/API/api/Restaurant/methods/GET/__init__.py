from ......framework import app, jwt, db, logger, t
from ......database.tables import restaurant

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Restaurant import RestaurantResponseSucces
from .....tags import RESTAURANT


@app.get('/api/admin/get/restaurant', tags=[RESTAURANT])
async def get_restaurant(hashf: str = Depends(jwt)) -> RestaurantResponseSucces:

    try: restaurant_data = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                        all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання даних закладу\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки запиту')
    
    if restaurant_data is None:
        raise HTTPException(status_code=403, detail="Відсутній ресторан в системі")

    return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(restaurant_data)})