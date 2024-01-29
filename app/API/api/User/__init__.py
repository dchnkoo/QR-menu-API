from ....framework import app, logger, db, t, jwt, jwt_validation
from fastapi import Depends

from ...ValidationModels.Register import RegisterUser
from ...ValidationModels.Login import LoginByLP

from ...ResponseModels.Login import SuccesLogin
from ...ResponseModels.Register import (RegisterResponseFail, RegisterResponseSucces)

from ....database.tables import (authefication, restaurant,
                                 categories, tables)


TAG = "User"

@app.post('/api/admin/register', tags=[TAG])
async def register(data: RegisterUser) -> (RegisterResponseSucces | RegisterResponseFail):

    """ 

    <h1>Реєстрація користувача</h1> 
    <p>Для реєстрації потрібен тільки email та password користувача, а також вказати срок дії JWT токену для його генерації.</p>
    <p>У випадку успішної реєстрації вам повертається обьєкт з згенерованим токеном який потрібно зберегти в cookie</p>
    <p>Ключ в cookie для JWT повинен бути <strong>token</strong></p>
    <br>
    <p>Обьєкт time має дефолтні значення 
    <strong>{</strong>&nbsp;&nbsp;
    type: "days", number: 1
    &nbsp;&nbsp;<strong>}</strong>
    тому за бажанням можете залишити цей обьєкт порожнім якщо вас влаштовує срок дії токену</p>

    
    """

    if await db.async_get_where(authefication, exp=authefication.c.email == data.email, all_=False):
        return {'status': 403, 'msg': f"{data.email} вже зареєстрований"}
    
    hashf = t.get_hash(data.email + data.password)
    password = t.get_hash(data.password)

    get_data = data.model_dump()
    get_data['hashf'] = hashf
    get_data['password'] = password

    time = get_data.pop('time')
    user = await db.async_insert_data(authefication, **get_data)

    playload = jwt.get_playload(user[0], user[2], **{time['type']: time['number']})
    token = jwt.get_token(**playload)
    jwt.save_token(token, user[1])

    return {'status': 200, 'token': token, 'user_data': t.parse_user_data(user._asdict())}


@app.post("/api/admin/login", tags=[TAG])
async def login(data: LoginByLP) -> (RegisterResponseSucces | RegisterResponseFail):
    """
    
    <h1>Логування користувача за email та password</h1>
    <p>Для створення JWT токену потрібно вказати time та зберегти виданний від серверу токен в cookie.</p>
    <p>time має дефолтне значення 
    <strong>{</strong>&nbsp;&nbsp;
    type: "days", number: 1
    &nbsp;&nbsp;<strong>}</strong>
    
    Якщо вас влаштовує строк дії токену можете залишати ключ time як порожній обьєкт</p>
    
    """

    email, password, time_type, time = data.email, data.password, data.time.type, data.time.number

    password = t.get_hash(password)

    user = await db.async_get_where(authefication, and__=(authefication.c.email == email,
                        authefication.c.password == password), all_=False)
    
    # Якщо користувач присутній в бд тоді генеруємо новий токен зберігаємо та повертаємо дані
    if user:
        playload = jwt.get_playload(user[0], user[2], **{time_type: time})
        token = jwt.get_token(**playload)
        jwt.save_token(token, user[1])

        return {"status": 200, "token": token, 'user_data': t.parse_user_data(user._asdict())}
    
    return {'status': 403, "msg": f"{email} користувач відсутній в системі"}


@app.get("/api/admin/login/token", tags=[TAG])
async def login_by_token(hashf: str = Depends(jwt_validation)) -> (SuccesLogin | RegisterResponseFail):

    """
    <h1>Логування в систему за допомогою JWT токену</h1>
    <p><strong>Щоб отримати данні користувача</strong> та виконати успішне логування у користувача в 
    <strong>cookie</strong> повинен знаходитись JWT токен. Він повинен бути дійсним та мати <strong>ключ token</strong> </p>
    """

    try: 
        user = await db.async_get_where(authefication, exp=authefication.c.hashf == hashf,
                        all_=False)
    
        return {'status': 200, 'user_data': t.parse_user_data(user._asdict())}
    except:
        logger.error(f"JWT {hashf} відстуній в JWTMetaData, але залишається дійсним")
        return {'status': 403, 'msg': 'Згенеруйте новий токен для користувача'}



@app.get("/api/admin/get-full-info/user", tags=[TAG])
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

    return {"status": 500} | result if "details" in result else {"status": 200, "data": result}


@app.delete('/api/admin/delete/session/user', tags=[TAG], dependencies=[Depends(jwt_validation)])
async def delete_user_from_session():
    """
    <h1>Вихід користувача з системи</h1>

    <p>Якщо потрібно вийти з аккаунту користувача потрібно відправити DELETE
    запит на цей url та обов'язково повинен бути токен в cookie. В іншому випадку
    буде помилка.</p>
    """