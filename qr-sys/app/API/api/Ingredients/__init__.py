from ....framework import app, jwt_validation, db, logger

from fastapi import Depends

from ...ValidationModels.Ingredients import IngredientScheme, DeleteIngredient

from ...ResponseModels.Ingredients import IngredientResponse, IngredientGetResponse
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import (restaurant, ingredients)



TAG = "Ingredients"

@app.post('/api/admin/add/ingredient', tags=[TAG])
async def add_ingredient(data: IngredientScheme, hashf: str = Depends(jwt_validation)) -> (IngredientResponse | RegisterResponseFail):
    dish_id = data.dish_id

    # отримуємо id ресторану
    try:
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання ресторану\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час отримання інформації ресторану'}

    # вставляємо дані в ingredient таблицю
    insert_ingredient = {'ingredient': data.ingredient, 'restaurant_id': restaurant_id, "dish_id": dish_id}
    try: new_ingredient = await db.async_insert_data(ingredients, **insert_ingredient)
    except Exception as e:
        logger.error(f"Помилка під час вставки інгредієнтів\n\nhahsf: {hashf}\nrestaurant_id: {restaurant_id}\nDish: {dish_id}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту'}
    
    return {'status': 200, 'ingredient': new_ingredient._asdict()}


@app.get('/api/admin/get/ingredients', tags=[TAG], dependencies=[Depends(jwt_validation)])
async def get_ingredients(dish_id: int) -> (IngredientGetResponse | RegisterResponseFail):

    try: ingredients_data = await db.async_get_where(ingredients, exp=ingredients.c.dish_id == dish_id, to_dict=True) 

    except Exception as e:
        logger.error(f"Помилка під час отримання інгредієнтів\n\ndish_id: {dish_id}\n\nError: {e}")
        return {"status": 500, "msg": "Невідома помилка під час обробки запиту"}

    return {"status": 200, "data": [i for i in ingredients_data if i]}


@app.delete("/api/admin/delete/ingredients", tags=[TAG], dependencies=[Depends(jwt_validation)])
async def delete_ingredients(data: DeleteIngredient) -> RegisterResponseFail:
    ingredient_id, dish_id = data.ingredient_id, data.dish_id

    try: await db.async_delete_data(ingredients, and__=(ingredients.c.id == ingredient_id,
                                                        ingredients.c.dish_id == dish_id))
    except Exception as e:
        logger.error(f"Помилка під час видалення ingredient_id: {ingredient_id}\n\nError: {e}")
        return {'status': 500, "msg": "Невідома помилка під час обробки запиту"}
    
    return {"status": 200, "msg": f"Інгредіент id: {ingredient_id} успішно видаленний"}