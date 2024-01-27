from ....framework import app, jwt, jwt_validation, db, logger

from fastapi import Depends

from ...ValidationModels.Ingredients import IngredientScheme

from ...ResponseModels.Ingredients import IngredientResponse
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import (restaurant, ingredients,
                                 dishIngredient, dishes)



TAG = "Ingredients"


@app.post('/api/admin/add/ingredient', tags=[TAG])
async def add_ingredient(data: IngredientScheme, token: str = Depends(jwt_validation)) -> (IngredientResponse | RegisterResponseFail):

    hashf = jwt.get_user_hash(token)
    dish_id = data.dish_id

    # отримуємо id ресторану
    try: restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf,
                                    all_=False)[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання ресторану\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час отримання інформації ресторану'}

    # вставляємо дані в ingredient таблицю
    insert_ingredient = {'ingredient': data.ingredient, 'restaurant_id': restaurant_id}
    try: new_ingredient = db.insert_data(ingredients, **insert_ingredient)
    except Exception as e:
        logger.error(f"Помилка під час вставки інгредієнтів\n\nhahsf: {hashf}\nrestaurant_id: {restaurant_id}\nDish: {dish_id}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту'}
    
    insert_dishingredient = {'ingredient_id': new_ingredient[0], 'dish_id': dish_id}
    try: db.insert_data(dishIngredient, **insert_dishingredient)
    except Exception as e:
        try: db.delete_data(ingredients, exp=ingredients.c.id == new_ingredient[0])
        except: pass

        logger.error(f"Помилка під час вставки данних в dishIngredient\n\nData: {insert_dishingredient | insert_ingredient}\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту'}

    try: get_dish = db.get_where(dishes, exp=dishes.c.id == dish_id,
                            all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання страви\n\nhashf: {hashf}\ndish_id: {dish_id}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту - можливо некоректний id страви спробуйте створити її заново'}
    
    return {'status': 200, 'ingredient': new_ingredient._asdict(), 'dish': get_dish}