from ......framework import app, logger, jwt_validation, db, t
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Restaurant import RestaurantRegister

from .....ResponseModels.Restaurant import (RestaurantResponseSucces)
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import restaurant 


TAG = "Restaurant"

@app.post('/api/admin/add/restaurant', tags=[TAG])
async def restaurant_add(data: RestaurantRegister, hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    """
    
    <h1>Створення закладу користувача</h1>
    <br>
    <p>Для використання цього та наступних методів у вас вже <strong>повнен</strong> бути в cookie JWT токен</p>
    
    """

    filter_data = {k: v for k, v in data.model_dump().items() if k != 'token'} | {'hashf': hashf}

    try: restaurant_data = await db.async_insert_data(restaurant, **filter_data)
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=400, content={'msg': 'Ресторан з таким користувачем вже інсує'})

    return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(restaurant_data._asdict())})


