from ......framework import app, logger, jwt_validation, db, t
from ......settings import MAX_WIDTH, MAX_HEIGHT

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Restaurant import RestaurantRegister

from .....ResponseModels.Restaurant import (RestaurantResponseSucces)
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import restaurant 
from .....tags import RESTAURANT


@app.post('/api/admin/add/restaurant', tags=[RESTAURANT])
async def restaurant_add(data: RestaurantRegister, hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    """
    
    <h1>Створення закладу користувача</h1>
    <br>
    <p>Для використання цього та наступних методів у вас вже <strong>повнен</strong> бути в cookie JWT токен</p>
    
    """

    restaurant_data = data.model_dump()

    if "logo" in restaurant_data and restaurant_data["logo"] is not None:
        status, code, msg = t.check_images_size(restaurant_data["logo"], MAX_WIDTH, MAX_HEIGHT)

        if status is False:
            raise HTTPException(status_code=code, detail=msg)

    filter_data = restaurant_data | {'hashf': hashf}

    try: restaurant_data = await db.async_insert_data(restaurant, **filter_data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=423, detail='Ресторан з таким користувачем вже інсує')

    return JSONResponse(status_code=200, content={'restaurant_data': t.parse_user_data(restaurant_data._asdict())})


