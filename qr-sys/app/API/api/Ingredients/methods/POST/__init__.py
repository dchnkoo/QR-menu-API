from ......framework import app, jwt_validation, db, logger

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Ingredients import IngredientScheme

from .....ResponseModels.Ingredients import Ingredient
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import (restaurant, ingredients)
from .....tags import INGREDIENTS


@app.post('/api/admin/add/ingredient', tags=[INGREDIENTS])
async def add_ingredient(data: IngredientScheme, hashf: str = Depends(jwt_validation)) -> (Ingredient | RegisterResponseFail):
    dish_id = data.dish_id

    # отримуємо id ресторану
    try:
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання ресторану\n\nhashf: {hashf}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Помилка під час отримання інформації ресторану')

    # вставляємо дані в ingredient таблицю
    insert_ingredient = {'ingredient': data.ingredient, 'restaurant_id': restaurant_id, "dish_id": dish_id}
    try: new_ingredient = await db.async_insert_data(ingredients, **insert_ingredient)
    except Exception as e:
        logger.error(f"Помилка під час вставки інгредієнтів\n\nhahsf: {hashf}\nrestaurant_id: {restaurant_id}\nDish: {dish_id}\n\nError: {e}")
        raise HTTPException(status_code=500, detail='Помилка під час обробки запиту')
    
    return JSONResponse(status_code=200, content=new_ingredient._asdict())

