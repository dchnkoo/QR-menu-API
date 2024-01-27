from ....framework import app, logger, jwt, jwt_validation, db, t
from fastapi import Depends

from ...ValidationModels.Restaurant import RestaurantRegister, RestaurantUpdate

from ...ResponseModels.Restaurant import (RestaurantResponseSucces)
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import authefication, restaurant 


TAG = "Restaurant"

@app.post('/api/admin/add/restaurant', tags=[TAG])
async def restaurant_add(data: RestaurantRegister, token: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    """
    
    Метод додає заклад користувача до бази даних, на одного користувача тільки один заклад,
    щоб виконати транзакцію потрібно використовувати тимчасовий токен користувача який видається
    при логуванні або реєстрації

    
    """

    try: user = db.get_where(authefication.c.hashf, exp=authefication.c.hashf == jwt.get_user_hash(token),
                        all_=False)
    except Exception as e: 
        logger.error(e) 
        return {'status': 500, 'msg': 'Невідома помилка. Спробуйте знову згенерувати токен'}

    # Отримуємо hash користувача
    hashf = user[0]
    filter_data = {k: v for k, v in data.model_dump().items() if k != 'token'} | {'hashf': hashf}

    try: restaurant_data = db.insert_data(restaurant, **filter_data)
    except Exception as e:
        logger.error(e)
        return {'status': 400, 'msg': 'Ресторан з таким користувачем вже інсує'}

    return {'status': 200, 'restaurant_data': t.parse_user_data(restaurant_data._asdict())}    


@app.delete('/api/admin/delete/restaurant', tags=[TAG])
async def restaurant_delete(token: str = Depends(jwt_validation)) -> RegisterResponseFail:
    
    hashf = jwt.get_user_hash(token)
    try:
        db.delete_data(restaurant, exp=restaurant.c.hashf == hashf)
    
    except Exception as e:
        logger.error(f"Сталась помилка при видаленні данних ресторану\n\nhashf: {hashf}\n\nError:\n\n{e}")
        return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}

    else:
        return {'status': 200, "msg": 'Ресторан видалений з системи'}

    


@app.patch('/api/admin/update/restaurant', tags=[TAG])
async def restaurant_data_update(data: RestaurantUpdate, token: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):

    hashf = jwt.get_user_hash(token)

    try: new_data = db.update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                **t.parse_user_data(data.model_dump()))
    except Exception as e:
        logger.error(f"Помилка при оновленні даннних закладу\n\nToken: {token}\n\nhashf: {hashf}\n\n Error: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}
    
    return {'status': 200, 'token': token, 'restaurant_data': t.parse_user_data(new_data._asdict())}



@app.get('/api/admin/get/restaurant', tags=[TAG])
async def get_restaurant(token: str = Depends(jwt_validation)) -> (RestaurantResponseSucces | RegisterResponseFail):
    hashf = jwt.get_user_hash(token)

    try: restaurant_data = db.get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                        all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання даних закладу\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'}
    

    logger.info(restaurant_data)
    return {'status': 200, "token": token, 'restaurant_data': t.parse_user_data(restaurant_data)}