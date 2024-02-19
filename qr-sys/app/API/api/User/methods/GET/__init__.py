from ......framework import jwt_validation, app, db, t, logger
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from ......database.tables import (authefication, restaurant, 
                                   tables, categories)

from .....ResponseModels.Register import RegisterResponseFail
from .....ResponseModels.Login import SuccesLogin

from fastapi import Depends
from .....tags import USER


@app.get("/api/admin/login/token", tags=[USER])
async def login_by_token(hashf: str = Depends(jwt_validation)) -> (SuccesLogin | RegisterResponseFail):

    """
    <h1>Логування в систему за допомогою JWT токену</h1>
    <p><strong>Щоб отримати данні користувача</strong> та виконати успішне логування у користувача в 
    <strong>cookie</strong> повинен знаходитись JWT токен. Він повинен бути дійсним та мати <strong>ключ token</strong> </p>
    """
    try: 
        user = await db.async_get_where(authefication, exp=authefication.c.hashf == hashf,
                        all_=False)

        return JSONResponse(status_code=200, content={'user_data': t.parse_user_data(user._asdict())})
    except:
        logger.error(f"JWT {hashf} відстуній в JWTMetaData, але залишається дійсним")
        raise HTTPException(status_code=403, detail='Згенеруйте новий токен для користувача')



@app.get("/api/admin/get-full-info/user", tags=[USER])
async def get_full_info_from_user(hashf: str = Depends(jwt_validation)):
    """
    <h1>Метод для отримання повної інформації про користувача</h1>
    <p>Метод повертає інформацію про аккаунт користувача, заклад, кількість столів та категорії.</p>
    <p>Якщо у користувача <strong>не створений</strong> заклад тоді метод повертає:</p>
    <span>
    <strong>{</strong>
    <br>&nbsp;&nbsp;&nbsp;
    "status": 500,
    <br>&nbsp;&nbsp;&nbsp;
    "details": "Відстунє достатньо інформації"
    <br><strong>}</strong></span>
    
    """
   
    from_user = await db.async_join_data(authefication, restaurant,
                                     table_2exp=restaurant.c.hashf == hashf, 
                                     exp=authefication.c.hashf == hashf)
    
    restaurant_id = from_user["restaurant"]["id"] if "restaurant" in from_user else None

    from_restaurant = await db.async_get_where(categories, exp=categories.c.restaurant_id == restaurant_id, 
                                               to_dict=True)


    table_count = await db.async_get_where(tables, exp=tables.c.restaurant_id == restaurant_id,
                                           all_=False, count=True)
    
    if "restaurant" in from_user:
        from_user["restaurant"]["categories"] = from_restaurant
        from_user["restaurant"]["tables"] = table_count[1] if table_count else 0
    
    result = from_user if from_user else {'details': "Відстунє достатньо інформації"}

    return JSONResponse(status_code=500 if "details" in result else 200, content=result)