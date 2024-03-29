from ......framework import app, jwt, logger, db
from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Category import CategoryDelType
from ......database.tables import (restaurant, categories)
from .....tags import CATEGORY

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete('/api/admin/delete/categories', tags=[CATEGORY])
async def delete_categories(type: CategoryDelType, category_id: int = 0, hashf: str = Depends(jwt)) -> RegisterResponseFail:

    """
    <h3>Видалення категорії аналогічно як зі столами також можете вказати "all" або "category" та конкретний id категорії</h3>
    
    """

    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False, to_dict=True)
        restaurant_id = restaurant_id.get("id")

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