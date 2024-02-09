from ......framework import app, jwt_validation, logger, db
from ......database.tables import restaurant

from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Register import RegisterResponseFail
from .....tags import RESTAURANT


@app.delete('/api/admin/delete/restaurant', tags=[RESTAURANT])
async def restaurant_delete(hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    
    try: await db.async_delete_data(restaurant, exp=restaurant.c.hashf == hashf)
    except Exception as e:
        logger.error(f"Сталась помилка при видаленні данних ресторану\n\nhashf: {hashf}\n\nError:\n\n{e}")
        return JSONResponse(status_code=500, content={'msg': 'Невідома помилка під час виконання операції'})

    else:
        return JSONResponse(status_code=200, content={"msg": 'Ресторан видалений з системи'})