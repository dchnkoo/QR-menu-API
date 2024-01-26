from ....framework import app, logger, jwt, db, t

from ...ValidationModels import (RestaurantRegister, RestaurantUpdate, JWT)
from ...ResponseModels import (RestaurantResponseSucces, RegisterResponseFail)

from ....database.tables import authefication, restaurant 

TAG = "Restaurant"

@app.post('/api/admin/add/restaurant', tags=[TAG])
async def restaurant_add(data: RestaurantRegister) -> (RestaurantResponseSucces | RegisterResponseFail):

    """
    
    Метод додає заклад користувача до бази даних, на одного користувача тільки один заклад,
    щоб виконати транзакцію потрібно використовувати тимчасовий токен користувача який видається
    при логуванні або реєстрації

    
    """

    token = data.token

    is_valid = jwt.check_token(token)

    if is_valid[0]:
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

        return {'status': 200, 'token': token, 'restaurant_data': t.parse_user_data(restaurant_data._asdict())}        

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    return {'status': 403, 'msg': is_valid[1]}


@app.delete('/api/admin/delete/restaurant', tags=[TAG])
async def restaurant_delete(token: JWT) -> RegisterResponseFail:
    token_ = token.token
    
    is_valid = jwt.check_token(token_)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token_)
        try:
            db.delete_data(restaurant, exp=restaurant.c.hashf == hashf)
        
        except Exception as e:
            logger.error(f"Сталась помилка при видаленні данних ресторану\n\nhashf: {hashf}\n\nError:\n\n{e}")
            return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}

        else:
            return {'status': 200, "msg": 'Ресторан видалений з системи'}

    try: jwt.delete_token(token_) 
    except: logger.error(f"JWT {token_[:10]} відсутній в JWTMetaData")
    
    return {'status': 403, 'msg': is_valid[1]}


@app.patch('/api/admin/update/restaurant', tags=[TAG])
async def restaurant_data_update(data: RestaurantUpdate) -> (RestaurantResponseSucces | RegisterResponseFail):
    
    token = data.token

    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)

        try: new_data = db.update_data(restaurant, exp=restaurant.c.hashf == hashf, 
                                  **t.parse_user_data(data.model_dump()))
        except Exception as e:
            logger.error(f"Помилка при оновленні даннних закладу\n\nToken: {token}\n\nhashf: {hashf}\n\n Error: {e}")
            return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}
        
        return {'status': 200, 'token': token, 'restaurant_data': t.parse_user_data(new_data._asdict())}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    
    return {'status': 403, 'msg': is_valid[1]}


@app.get('/api/admin/get/restaurant/{token}', tags=[TAG])
async def get_restaurant(token: str) -> (RestaurantResponseSucces | RegisterResponseFail):
    
    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)

        try: restaurant_data = db.get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                            all_=False, to_dict=True)
        except Exception as e:
            logger.error(f"Помилка під час отримання даних закладу\n\nhashf: {hashf}\n\nError: {e}")
            return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'}
        

        logger.info(restaurant_data)
        return {'status': 200, "token": token, 'restaurant_data': t.parse_user_data(restaurant_data)}


    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    
    return {'status': 403, 'msg': is_valid[1]}