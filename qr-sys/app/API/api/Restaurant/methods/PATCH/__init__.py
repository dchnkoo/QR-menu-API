from ......framework import app, jwt_validation, t, db, logger
from ......database.tables import restaurant

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Restaurant import RestaurantUpdate
from .....ResponseModels.Restaurant import RestaurantResponseSucces
from .....ResponseModels.Register import RegisterResponseFail

from ...tags.tags import RESTAURANT


@app.patch('/api/admin/update/restaurant', tags=[RESTAURANT])
async def restaurant_data_update(data: RestaurantUpdate, hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    try: new_data = await db.async_update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                **t.parse_user_data(data.model_dump()))
    except Exception as e:
        logger.error(f"Помилка при оновленні даннних закладу\n\nhashf: {hashf}\n\n Error: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час виконання операції'})
    
    return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(new_data._asdict())})