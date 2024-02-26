from .....ResponseModels.Register import RegisterResponseFail
from ......framework import app, jwt_validation, db, logger
from ......database.tables import dishes
from .....tags import DISHES

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete('/api/admin/delete/dish', tags=[DISHES], dependencies=[Depends(jwt_validation)])
async def delete_dish(dish_id: int, category_id: int) -> RegisterResponseFail:
    dish, category = dish_id, category_id

    try: await db.async_delete_data(dishes, and__=(dishes.c.id == dish,
                                        dishes.c.category_id == category))
    except Exception as e:
        logger.error(f"Помилка під час видалення страви id: {dish} з категорії id: {category}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час видалення страви')

    return JSONResponse(status_code=200, content={'msg': f'Страва id: {dish} видаленна успішно з категорії id: {category}'})