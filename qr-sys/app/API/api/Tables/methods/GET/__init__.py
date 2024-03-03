from ......framework import app, jwt, logger, db, qr
from .....ResponseModels.Tables import GetTablesResponse
from ......database.tables import restaurant
from .....tags import TABLES

from fastapi.exceptions import HTTPException
from fastapi import Depends


@app.get('/api/admin/get/tables', tags=[TABLES])
async def get_tables(page: int = 1, hashf: str = Depends(jwt)) -> GetTablesResponse:
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання столів\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки запиту')

    return await qr.get_tables(restaurant_id, page)