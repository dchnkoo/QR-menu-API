from ....framework import app, logger, db, t, jwt

from ...ValidationModels.Register import RegisterUser
from ...ValidationModels.Login import Login
from ...ResponseModels.Register import (RegisterResponseFail, RegisterResponseSucces)

from ....database.tables import authefication


TAG = "User"

@app.post('/api/admin/register', tags=[TAG])
async def register(data: RegisterUser) -> (RegisterResponseSucces | RegisterResponseFail):

    """ 

    Метод приймає обьєкт 
    { 
        email: <пошта коритувача>,
        password: <пароль користувача>,
        time: по дефолту має значення   type: 'days', 
                                        number: 1.0     <-- Він визначає час дії JWT токену, замість days
                                                        ви можете вказати інші ключи такі як:
                                                        hours, minutes, weeks та значення обов'язково
                                                        повинно бути число типу float 
    } 
    
    """

    if db.get_where(authefication, exp=authefication.c.email == data.email, all_=False):
        return {'status': 403, 'msg': f"{data.email} вже зареєстрований"}
    
    hashf = t.get_hash(data.email + data.password)
    password = t.get_hash(data.password)

    get_data = data.model_dump()
    get_data['hashf'] = hashf
    get_data['password'] = password

    time = get_data.pop('time')
    user = db.insert_data(authefication, **get_data)

    playload = jwt.get_playload(user[0], user[2], **{time['type']: time['number']})
    token = jwt.get_token(**playload)
    jwt.save_token(token, user[1])

    return {'status': 200, 'token': token, 'user_data': t.parse_user_data(user._asdict())}


@app.post("/api/admin/login", tags=[TAG])
async def login(data: Login) -> (RegisterResponseSucces | RegisterResponseFail):
    """
    
    Метод логує користувача до системи якщо {type: login} потрібно буде вказати 
    ключ data в якому будуе обьект з ключами email, password та time для генерації новго JWT токену

    У випадку якщо {type: token} тоді логування відбувається за JWT токеном і в data треба буде вказати
    обьект тільки з одною парою ключ = значення {token: <токен користувача>}
    
    """


    if data.type == 'login':
        # Якщо тип входу є логін тоді отримуємо дані користувача
        email, password, time_type, time = data.data.email, data.data.password, data.data.time.type, data.data.time.number

        password = t.get_hash(password)

        user = db.get_where(authefication, and__=(authefication.c.email == email,
                            authefication.c.password == password), all_=False)
        
        # Якщо користувач присутній в бд тоді генеруємо новий токен зберігаємо та повертаємо дані
        if user:
            playload = jwt.get_playload(user[0], user[2], **{time_type: time})
            token = jwt.get_token(**playload)
            jwt.save_token(token, user[1])

            return {"status": 200, "token": token, 'user_data': t.parse_user_data(user._asdict())}
        
        return {'status': 403, "msg": f"{email} користувач відсутній в системі"}

    # Якщо логування по токену
    token = data.data.token

    is_valid = jwt.check_token(token)

    if is_valid[0]:
        try: 
            user = db.get_where(authefication, exp=authefication.c.hashf == jwt.get_user_hash(token),
                            all_=False)
        
            return {'status': 200, 'token': token, 'user_data': t.parse_user_data(user._asdict())}
        except:
            logger.error(f"JWT {token[:10]} відстуній в JWTMetaData, але залишається дійсним")
            return {'status': 403, 'msg': 'Згенеруйте новий токен для користувача'}

    try: jwt.delete_token(token) 
    except: logger.error(f"JWT {token[:10]} відсутній в JWTMetaData")

    return {'status': 403, 'msg': is_valid[1]}