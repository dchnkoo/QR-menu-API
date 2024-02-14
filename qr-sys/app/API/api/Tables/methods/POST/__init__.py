from ......framework import app, jwt_validation, db, qr, logger
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Tables import CreateTable
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant)
from .....tags import TABLES


@app.post('/api/admin/create/tables', tags=[TABLES])
async def add_tables(data: CreateTable, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    num, logo, background, fill = data.table_number, data.logo, data.background, data.fill_lines

    try: 
        get_restaurant = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf, all_=False)
        restaurant_id = get_restaurant[0]
        name = get_restaurant[2]


        try:
            image = get_restaurant[8]
            
            # if logo = True in request get logo
            if logo:
                if image is None or not image:
                    raise HTTPException(status_code=428, detail="Відсутній логотип для додавання його в QR код")
                logo = image

        except Exception as e:
            logger.error(f"Помилка під час обробки лого для QR-code\n\nRestaurant: name={name}, id={restaurant_id}\nError: {e}")
            raise HTTPException(status_code=415, detail="Помилка пов'язана з неправильним форматом логотипу.")

    except Exception as e:
        logger.error(f"Помилка під час пошуку id закладу\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час транзакції')
    
    try: qr.threads(qr.generate, name, restaurant_id, num, logo, background, fill)
    except Exception as e:
        logger.error(f"Помилка під час створення столів\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час транзакції')

    return JSONResponse(status_code=200, content={'msg': 'Столи та QR генеруються це може зайнятий деякий час'})

    


