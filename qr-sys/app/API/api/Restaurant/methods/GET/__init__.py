from ......framework import app, jwt_validation, db, logger, t
from ......database.tables import restaurant

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Restaurant import RestaurantResponseSucces
from .....ResponseModels.Register import RegisterResponseFail

from ...tags.tags import RESTAURANT


@app.get('/api/admin/get/restaurant', tags=[RESTAURANT])
async def get_restaurant(hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    try: restaurant_data = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                        all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання даних закладу\n\nhashf: {hashf}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час обробки запиту'})
    
    try: return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(restaurant_data)})
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(status_code=403, content={"msg": "Відсутній ресторан в системі"})