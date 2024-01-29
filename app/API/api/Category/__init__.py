from ....framework import app, jwt_validation, logger, db, t
from fastapi import Depends

from ...ValidationModels.Category import CategorySet, CategoryDelete

from ...ResponseModels.Category import (CategoryAddResponse, GetCategories)
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import (restaurant, categories, dishes,
                                 ingredients)


TAG = "Category"

@app.post('/api/admin/add/category', tags=[TAG])
async def add_category(data: CategorySet, hashf: str = Depends(jwt_validation)) -> (CategoryAddResponse | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки транзакції'}
    
    data_ = {k: v for k, v in data.model_dump().items() if k != 'token'} | {'restaurant_id': restaurant_id}

    try: new_category = await db.async_insert_data(categories, **data_)
    except Exception as e: 
        logger.error(f"Помилка під час додавання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\ndata: {data_}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту'}

    return {'status': 200, 'category': new_category._asdict()}


@app.get('/api/admin/get/categories', tags=[TAG])
async def get_categories(hashf: str = Depends(jwt_validation)) -> (GetCategories | RegisterResponseFail):
    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки транзакції'}


    try: category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                    to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
        return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}
    

    return {'status': 200, 'categories': category}


@app.delete('/api/admin/delete/categories', tags=[TAG])
async def delete_categories(data: CategoryDelete, hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:

    """
    <h3>Видалення категорії аналогічно як зі столами також можете вказати "all" або конкретний id категорії</h3>
    
    """

    type_ = data.delete.type

    try: 
        restaurant_id = await db.async_get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)
        restaurant_id = restaurant_id[0]

    except Exception as e:
        logger.error(f"Помилка під час отримання id закладу\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'} 


    match type_:

        case "category":
            category = data.delete.category_id

            try: await db.async_delete_data(categories, and__=(categories.c.restaurant_id == restaurant_id,
                                                    categories.c.id == category))
            except Exception as e:
                logger.error(f"Помилка під час видалення категорії id: {category}\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}

            return {"status": "200", 'msg': f'Категорія id: {category} була видаленна з системи'}
        case "all":
            try: await db.async_delete_data(categories, exp=categories.c.restaurant_id == restaurant_id)
            except Exception as e:
                logger.error(f"Помилка під час видалення категорій\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}
            
            return {"status": 200, "msg": f"Всі категорії були видаленні."}
        case _:
            return {'status': 403, 'msg': f"Невідомий тип для обробки запиту - {type_}"}
        

@app.get("/api/admin/get-full-info/categories", tags=[TAG])
async def get_full_info_categories(hashf: str = Depends(jwt_validation)):
    
    restaurant_ = await db.async_get_where(restaurant, exp=restaurant.c.hashf == hashf,
                                           all_=False, to_dict=True)
    
    if restaurant_ is None:
        return {"status": 500, "msg": "Неможливо виконати запит через відсутність зарєстрованого закладу у користувача"}

    restaurant_ = t.parse_user_data(restaurant_)

    restaurant_id = restaurant_['id']
    
    category = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                        to_dict=True)
    
    info = {"restaurant": restaurant_ | {"categories": category}}

    if category:
        dishes_data = await db.async_get_where(dishes, exp=dishes.c.restaurant_id == restaurant_id,
                                               to_dict=True)
        
        ingredients_data = await db.async_get_where(ingredients, exp=ingredients.c.restaurant_id == restaurant_id,
                                                    to_dict=True)
        
        for i in range(len(category)):
            category_id = category[i]["id"]
            category[i]["dishes"] = []
            
            for j in range(len(dishes_data)):
                category_dish_id = dishes_data[j]["category_id"]
                dishes_data[j]["ingredients"] = []

                if category_id == category_dish_id:
                    category[i]["dishes"].append(dishes_data[j])

                for l in range(len(ingredients_data)):

                    dish_id = dishes_data[j]["id"]
                    ingredients_id = ingredients_data[l]["dish_id"]

                    if dish_id == ingredients_id:
                        dishes_data[j]["ingredients"].append(ingredients_data[l])


    return info