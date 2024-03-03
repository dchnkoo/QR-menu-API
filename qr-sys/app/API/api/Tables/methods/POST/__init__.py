from ......framework import app, jwt, db, qr, logger
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Tables import CreateTable

from ......database.tables import (restaurant)
from .....tags import TABLES


@app.post('/api/admin/create/tables', tags=[TABLES])
async def add_tables(data: CreateTable, hashf: str = Depends(jwt)) -> RegisterResponseFail:
    num, logo, background, fill = data.table_number, data.logo, data.background, data.fill_lines

    get_restaurant = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf, all_=False, to_dict=True)

    if get_restaurant is None:
        raise HTTPException(status_code=412, detail="Для створення столів та QR потрібно зареєструвати заклад")
    
    restaurant_id = get_restaurant.get("id")
    name = get_restaurant.get("name")
    
    # Якщо користувач хоче додати лого до QR перевіряємо його наявність
    if logo:
        image = get_restaurant.get("logo")

        if image is None:
            raise HTTPException(status_code=415, detail="Відсутній логотип для додавння його до QR")

        logo = image

    try: qr.threads(qr.generate, name, restaurant_id, num, logo, background, fill)
    except Exception as e:
        logger.error(f"Помилка під час створення столів\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час транзакції')

    return JSONResponse(status_code=200, content={'msg': 'Столи та QR генеруються це може зайнятий деякий час'})