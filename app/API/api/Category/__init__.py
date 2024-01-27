from ....framework import app, jwt, jwt_validation, logger, db
from fastapi import Depends

from ...ValidationModels.Category import CategorySet, CategoryDelete

from ...ResponseModels.Category import (CategoryAddResponse, GetCategories)
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import (restaurant, categories)


TAG = "Category"

@app.post('/api/admin/add/category', tags=[TAG])
async def add_category(data: CategorySet, token: str = Depends(jwt_validation)) -> (CategoryAddResponse | RegisterResponseFail):

    hashf = jwt.get_user_hash(token)

    try: restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки транзакції'}
    
    data_ = {k: v for k, v in data.model_dump().items() if k != 'token'} | {'restaurant_id': restaurant_id}

    try: new_category = db.insert_data(categories, **data_)
    except Exception as e: 
        logger.error(f"Помилка під час додавання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\ndata: {data_}\n\nError: {e}")
        return {'status': 500, 'msg': 'Помилка під час обробки запиту'}

    return {'status': 200, 'category': new_category._asdict()}


@app.get('/api/admin/get/categories', tags=[TAG])
async def get_categories(token: str = Depends(jwt_validation)) -> (GetCategories | RegisterResponseFail):
    
    hashf = jwt.get_user_hash(token)

    try: restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання restaurant_id\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки транзакції'}


    try: category = db.get_where(categories, exp=categories.c.restaurant_id == restaurant_id,
                                    to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання категорії\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
        return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}
    

    return {'status': 200, 'categories': category}


@app.delete('/api/admin/delete/categories', tags=[TAG])
async def delete_categories(data: CategoryDelete, token: str = Depends(jwt_validation)) -> RegisterResponseFail:

    type_ = data.delete.type
    hashf = jwt.get_user_hash(token)

    try: restaurant_id = db.get_where(restaurant.c.id, exp=restaurant.c.hashf == hashf, 
                                    all_=False)[0]
    except Exception as e:
        logger.error(f"Помилка під час отримання id закладу\n\nhashf: {hashf}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки запиту'} 


    match type_:

        case "category":
            category = data.delete.category_id

            try: db.delete_data(categories, and__=(categories.c.restaurant_id == restaurant_id,
                                                    categories.c.id == category))
            except Exception as e:
                logger.error(f"Помилка під час видалення категорії id: {category}\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}

            return {"status": "200", 'msg': f'Категорія id: {category} була видаленна з системи'}
        case "all":
            try: db.delete_data(categories, exp=categories.c.restaurant_id == restaurant_id)
            except Exception as e:
                logger.error(f"Помилка під час видалення категорій\n\nhashf: {hashf}\n\nrestautant_id: {restaurant_id}\n\nError: {e}")
                return {'status': 500, 'msg': "Невідома помилка під час обробки запиту"}
            
            return {"status": 200, "msg": f"Всі категорії були видаленні з сессії {token[:10]}"}
        case _:
            return {'status': 403, 'msg': f"Невідомий тип для обробки запиту - {type_}"}