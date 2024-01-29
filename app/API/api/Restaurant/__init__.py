from ....framework import app, logger, jwt_validation, db, t
from fastapi import Depends

from ...ValidationModels.Restaurant import RestaurantRegister, RestaurantUpdate

from ...ResponseModels.Restaurant import (RestaurantResponseSucces)
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import restaurant 


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
        return {'status': 400, 'msg': 'Ресторан з таким користувачем вже інсує'}

    return {'status': 200, 'restaurant_data': t.parse_user_data(restaurant_data._asdict())}    


@app.delete('/api/admin/delete/restaurant', tags=[TAG])
async def restaurant_delete(hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    
    try: await db.async_delete_data(restaurant, exp=restaurant.c.hashf == hashf)
    except Exception as e:
        logger.error(f"Сталась помилка при видаленні данних ресторану\n\nhashf: {hashf}\n\nError:\n\n{e}")
        return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}

    else:
        return {'status': 200, "msg": 'Ресторан видалений з системи'}

    


@app.patch('/api/admin/update/restaurant', tags=[TAG])
async def restaurant_data_update(data: RestaurantUpdate, hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    try: new_data = await db.async_update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                **t.parse_user_data(data.model_dump()))
    except Exception as e:
        logger.error(f"Помилка при оновленні даннних закладу\n\nhashf: {hashf}\n\n Error: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}
    
    return {'status': 200, 'restaurant_data': t.parse_user_data(new_data._asdict())}



@app.get('/api/admin/get/restaurant', tags=[TAG])
async def get_restaurant(hashf: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    try: restaurant_data = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                        all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання даних закладу\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'}
    

    try: return {'status': 200, 'restaurant_data': t.parse_user_data(restaurant_data)}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"status": 403, "msg": "Відсутній ресторан в системі"}