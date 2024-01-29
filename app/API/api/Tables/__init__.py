from ....framework import app, jwt_validation, db, qr, logger
from fastapi import Depends

from ...ValidationModels.Tables import CreateTable, DeleteTable

from ...ResponseModels.Tables import GetTablesResponse
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import (restaurant)



TAG = "Tables"

@app.post('/api/admin/create/tables', tags=[TAG])
async def add_tables(data: CreateTable, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    num = data.table_number

    try: 
        get_restaurant = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf, all_=False)
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

    


@app.delete('/api/admin/delete/tables', tags=[TAG])
async def delete_tables(data: DeleteTable, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:

    """
    
    <h1>Видалення столів</h1>
    <br>
    <p>У вас пристуні дв варіанти видалення столів.</p>
    <p><br>Перший варіант:<br><strong>{</strong><br>
    &nbsp;&nbsp;"type": "table", <-- Видаляє конкретний стіл за його номером
    <br>&nbsp;&nbsp; ...
    <br><strong>}</strong></p>

    <p>Другий варіант:<br><strong>{</strong><br>
    &nbsp;&nbsp;"type": "all" <-- Видаляє всі столи
    <br><strong>}</strong></p>

    """

    type_ = data.data.type

    restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, all_=False)
    restaurant_id = restaurant_id[0]
    
    match type_:

        case 'all':
            try: qr.threads(qr.delete_all, (restaurant_id))
            except Exception as e:
                logger.error(f"Помилка при видаленні всіх столів\n\nhashf: {hashf}\n\nError: {e}")
                return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}

            return {'status': 200, 'msg': f'Видаленні всі столи.'}
        case 'table':
            table_num = data.data.table_number

            try: await qr.delete_table(restaurant_id, table_num)
            except Exception as e:
                logger.error(f"Невідома помилка під час видалення столу\n\nhashf: {hashf}\n\nError: {e}")
                return {'status': 500, 'msg': 'Невідома помилка під час транзакції'}

            return {'status': 200, 'msg': f'Видаленний стіл - номер: {table_num}.'}
        case _:
            return {'status': 400, 'msg': f'Некоректний тип видалення {type_}'}


@app.get('/api/admin/get/tables', tags=[TAG])
async def get_tables(page: int = 1, hashf: str = Depends(jwt_validation)) -> (GetTablesResponse | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання столів\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'}

    return await qr.get_tables(restaurant_id, page)

