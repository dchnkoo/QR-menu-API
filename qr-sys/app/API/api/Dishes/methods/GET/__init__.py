from ......framework import app, jwt, db, logger
from .....ResponseModels.Dishes import DishResponseList
from ......database.tables import dishes
from .....tags import DISHES

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.get('/api/admin/get/dish', tags=[DISHES], dependencies=[Depends(jwt)])
async def get_dishes(category_id: int) -> DishResponseList:
    try: data = await db.async_get_where(dishes, exp=dishes.c.category_id == category_id, 
                                to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання страв\n\nid Категорії: {category_id}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки транзакції')
    
    return JSONResponse(status_code=200, content={"data": data})