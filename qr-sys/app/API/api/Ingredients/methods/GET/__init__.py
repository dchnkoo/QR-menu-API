from ......framework import app, jwt_validation, db, logger

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Ingredients import IngredientGetResponse
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import ingredients
from .....tags import INGREDIENTS


@app.get('/api/admin/get/ingredients', tags=[INGREDIENTS], dependencies=[Depends(jwt_validation)])
async def get_ingredients(dish_id: int) -> (IngredientGetResponse | RegisterResponseFail):

    try: ingredients_data = await db.async_get_where(ingredients, exp=ingredients.c.dish_id == dish_id, to_dict=True) 

    except Exception as e:
        logger.error(f"Помилка під час отримання інгредієнтів\n\ndish_id: {dish_id}\n\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки запиту")

    return JSONResponse(status_code=200, content={"data": [i for i in ingredients_data if i]})