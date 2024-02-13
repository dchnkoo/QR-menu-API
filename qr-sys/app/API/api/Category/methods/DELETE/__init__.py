from ......framework import app, jwt_validation, logger, db

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant, categories)
from .....tags import CATEGORY


@app.delete('/api/admin/delete/categories', tags=[CATEGORY])
async def delete_categories(type: str = "category", category_id: int = 0, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:

    """
    <h3>Видалення категорії аналогічно як зі столами також можете вказати "all" або конкретний id категорії</h3>
    
    """

    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]

    except Exception as e:
        logger.error(f"Помилка під час отримання id закладу\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Невідома помилка під час обробки запиту')

    match type:

        case "category":
            try: await db.async_delete_data(categories, and__=(categories.c.restaurant_id == restaurant_id,
                                                    categories.c.id == category_id))
            except Exception as e:
                logger.error(f"Помилка під час видалення категорії id: {category_id}\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                raise HTTPException(status_code=500, detail="Невідома помилка під час обробки запиту")

            return JSONResponse(status_code=200, content={'msg': f'Категорія id: {category_id} була видаленна з системи'})
        case "all":
            try: await db.async_delete_data(categories, exp=categories.c.restaurant_id == restaurant_id)
            except Exception as e:
                logger.error(f"Помилка під час видалення категорій\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                raise HTTPException(status_code=500, detail="Невідома помилка під час обробки запиту")
            
            return JSONResponse(status_code=200, content={"msg": "Всі категорії були видаленні."})
        case _:
            raise HTTPException(status_code=403, detail=f"Невідомий тип для обробки запиту - {type}")