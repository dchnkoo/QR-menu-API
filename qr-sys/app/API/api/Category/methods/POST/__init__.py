from ......framework import app, jwt_validation, logger, db

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Category import CategorySet
from .....ResponseModels.Category import CategoryTable
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant, categories)
from .....tags import CATEGORY


@app.post('/api/admin/add/category', tags=[CATEGORY])
async def add_category(data: CategorySet, hashf: str = Depends(jwt_validation)) -> (CategoryTable | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки транзакції')
    
    data_ = data.model_dump()| {'restaurant_id': restaurant_id}

    try: new_category = await db.async_insert_data(categories, **data_)
    except Exception as e: 
        logger.error(f"Помилка під час додавання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\ndata: {data_}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Помилка під час обробки запиту')

    return JSONResponse(status_code=200, content=new_category._asdict())