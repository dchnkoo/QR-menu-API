from ......framework import app, jwt_validation, db, qr, logger
from ......database.tables import restaurant

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Tables import DeleteType
from .....ResponseModels.Register import RegisterResponseFail
from .....tags import TABLES


@app.delete('/api/admin/delete/tables', tags=[TABLES])
async def delete_tables(type: DeleteType, table_number: int = 0, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:

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

    restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, all_=False)
    restaurant_id = restaurant_id[0]
    
    match type:

        case 'all':
            try: qr.threads(qr.delete_all, (restaurant_id))
            except Exception as e:
                logger.error(f"Помилка при видаленні всіх столів\n\nhashf: {hashf}\n\nError: {e}")
                raise HTTPException(status_code=500, detail='Невідома помилка під час транзакції')

            return JSONResponse(status_code=200, content={'msg': 'Видаленні всі столи.'})
        case 'table':
            try: await qr.delete_table(restaurant_id, table_number)
            except Exception as e:
                logger.error(f"Невідома помилка під час видалення столу\n\nhashf: {hashf}\n\nError: {e}")
                raise HTTPException(status_code=500, detail='Невідома помилка під час транзакції')

            return JSONResponse(status_code=200, content={'msg': f'Видаленний стіл - номер: {table_number}.'})
        case _:
            raise HTTPException(status_code=400, detail=f'Некоректний тип видалення {type}')