from ......framework import app, jwt_validation, db, qr, logger

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Tables import CreateTable
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant)
from .....tags import TABLES


@app.post('/api/admin/create/tables', tags=[TABLES])
async def add_tables(data: CreateTable, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    num = data.table_number

    try: 
        get_restaurant = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf, all_=False)
        restaurant_id = get_restaurant[0]
        name = get_restaurant[2]
    except Exception as e:
        logger.error(f"Помилка під час пошуку id закладу\n\nhashf: {hashf}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час транзакції'})
    
    try: qr.threads(qr.generate, name, restaurant_id, num)
    except Exception as e:
        logger.error(f"Помилка під час створення столів\n\nhashf: {hashf}\n\nError: {e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час транзакції'})

    return JSONResponse(status_code=200, content={'msg': 'Столи та QR генеруються це може зайнятий деякий час'})

    


