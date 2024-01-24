from app.framework import app, db, t, jwt, logger, qr

from .ValidationModels import (RegisterUser, Login, RestaurantRegister, RestaurantUpdate,
                               JWT, CreateTable, DeleteTable)
from .ResponseModels import (RegisterResponseFail, RegisterResponseSucces,
                             RestaurantResponseSucces)

from ..database.tables import (authefication, restaurant,
                               categories, dishes, ingredients,
                               dishIngredient, tables)


@app.post('/api/admin/register')
async def register(data: RegisterUser) -> (RegisterResponseSucces | RegisterResponseFail):

    """ 

    Метод приймає обьєкт 
    { 
        email: <пошта коритувача>,
        password: <пароль користувача>,
        time: по дефолту має значення   type: 'days', 
                                        number: 1.0     <-- Він визначає час дії JWT токену, замість days
                                                        ви можете вказати інші ключи такі як:
                                                        hours, minutes, weeks та значення обов'язково
                                                        повинно бути число типу float 
    } 
    
    """

    if db.get_where(authefication, exp=authefication.c.email == data.email, all_=False):
        return {'status': 403, 'msg': f"{data.email} вже зареєстрований"}
    
    hashf = t.get_hash(data.email + data.password)
    password = t.get_hash(data.password)

    get_data = data.model_dump()
    get_data['hashf'] = hashf
    get_data['password'] = password

    time = get_data.pop('time')
    user = db.insert_data(authefication, **get_data)

    playload = jwt.get_playload(user[0], user[2], **{time['type']: time['number']})
    token = jwt.get_token(**playload)
    jwt.save_token(token, user[1])

    return {'status': 200, 'token': token, 'user_data': t.parse_user_data(user._asdict())}


@app.post("/api/admin/login")
async def login(data: Login) -> (RegisterResponseSucces | RegisterResponseFail):
    """
    
    Метод логує користувача до системи якщо {type: login} потрібно буде вказати 
    ключ data в якому будуе обьект з ключами email, password та time для генерації новго JWT токену

    У випадку якщо {type: token} тоді логування відбувається за JWT токеном і в data треба буде вказати
    обьект тільки з одною парою ключ = значення {token: <токен користувача>}
    
    """


    if data.type == 'login':
        # Якщо тип входу є логін тоді отримуємо дані користувача
        email, password, time_type, time = data.data.email, data.data.password, data.data.time.type, data.data.time.number

        password = t.get_hash(password)

        user = db.get_where(authefication, and__=(authefication.c.email == email,
                            authefication.c.password == password), all_=False)
        
        # Якщо користувач присутній в бд тоді генеруємо новий токен зберігаємо та повертаємо дані
        if user:
            playload = jwt.get_playload(user[0], user[2], **{time_type: time})
            token = jwt.get_token(**playload)
            jwt.save_token(token, user[1])

            return {"status": 200, "token": token, 'user_data': t.parse_user_data(user._asdict())}
        
        return {'status': 403, "msg": f"{email} користувач відсутній в системі"}

    # Якщо логування по токену
    token = data.data.token

    is_valid = jwt.check_token(token)

    if is_valid[0]:
        try: 
            user = db.get_where(authefication, exp=authefication.c.hashf == jwt.get_user_hash(token),
                            all_=False)
        
            return {'status': 200, 'token': token, 'user_data': t.parse_user_data(user._asdict())}
        except:
            logger.error(f"JWT {token[:10]} відстуній в JWTMetaData, але залишається дійсним")
            return {'status': 403, 'msg': 'Згенеруйте новий токен для користувача'}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")

    return {'status': 403, 'msg': is_valid[1]}


@app.post('/api/admin/add/restaurant')
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


@app.post('/api/admin/delete/restaurant')
async def restaurant_delete(token: JWT) -> RegisterResponseFail:
    
    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)
        try:
            db.delete_data(restaurant, exp=restaurant.c.hashf == hashf)
        
        except Exception as e:
            logger.error(f"Сталась помилка при видаленні данних ресторану\n\nhashf: {hashf}\n\nError:\n\n{e}")
            return {'status': 500, 'msg': 'Невідома помилка під час виконання операції'}

        else:
            return {'status': 200, "msg": 'Ресторан видалений з системи'}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    return {'status': 403, 'msg': is_valid[1]}


@app.post('/api/admin/update/restaurant')
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
    else: return {'status': 403, 'msg': is_valid[1]}


@app.post('/api/admin/create/tables')
async def add_tables(data: CreateTable) -> RegisterResponseFail:
    token, num = data.token, data.table_number

    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)

        try: 
            get_restaurant = db.get_where(restaurant, exp=restaurant.c.hashf == hashf, all_=False)
            restaurant_id = get_restaurant[0]
            name = get_restaurant[2]
        except Exception as e:
            logger.error(f"Помилка під час пошуку id закладу\n\nhashf: {hashf}\n\nError: {e}")
            return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}
        
        try: qr.threads(qr.generate, name, restaurant_id, num)
        except Exception as e:
            logger.error(f"Помилка під час створення столів\n\nhashf: {hashf}\n\nError: {e}")
            return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}

        return {'status': 200, 'msg': 'Столи та QR генеруються це може зайнятий деякий час'}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    return {'status': 403, 'msg': is_valid[1]}


@app.post('/api/admin/delete/tables')
async def delete_tables(data: DeleteTable) -> RegisterResponseFail:
    token, type_ = data.token, data.data.type

    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)

        restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, all_=False)[0]
        match type_:

            case 'all':
                try: qr.threads(qr.delete_all, (restaurant_id))
                except Exception as e:
                    logger.error(f"Помилка при видаленні всіх столів\n\nhashf: {hashf}\n\nError: {e}")
                    return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}

                return {'status': 200, 'msg': f'Видаленні всі столи. Сессія {token[:10]}'}
            case 'table':
                table_num = data.data.table_number

                try: qr.delete_table(restaurant_id, table_num)
                except Exception as e:
                    logger.error(f"Невідома помилка під час видалення столу\n\nhashf: {hashf}\n\nError: {e}")
                    return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}

                return {'status': 200, 'msg': f'Видаленний стіл - номер: {table_num}. Сессія {token[:10]}'}
            case _:
                return {'status': 400, 'msg': f'Некоректний тип видалення {type_}'}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    return {'status': 403, 'msg': is_valid[1]}