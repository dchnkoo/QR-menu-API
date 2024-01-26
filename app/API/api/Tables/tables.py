from ....framework import app, jwt, db, qr, logger

from ...ValidationModels import (CreateTable, DeleteTable)
from ...ResponseModels import (GetTablesResponse, RegisterResponseFail)

from ....database.tables import (restaurant)



TAG = "Tables"

@app.post('/api/admin/create/tables', tags=[TAG])
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


@app.delete('/api/admin/delete/tables', tags=[TAG])
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


@app.get('/api/admin/get/tables/{token}', tags=[TAG])
async def get_tables(token: str, page: int = 1) -> (GetTablesResponse | RegisterResponseFail):
    is_valid = jwt.check_token(token)

    if is_valid[0]:
        hashf = jwt.get_user_hash(token)

        try: restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                     all_=False)[0]
        except Exception as e:
            logger.error(f"Помилка під час отримання столів\n\nhashf: {hashf}\n\nError: {e}")
            return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'}

        return qr.get_tables(restaurant_id, page)

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")
    return {'status': 403, 'msg': is_valid[1]}