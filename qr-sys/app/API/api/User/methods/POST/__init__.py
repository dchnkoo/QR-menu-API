from ......framework import app, db, t, jwt, recovery, send_mail, logger
from fastapi.responses import JSONResponse

from .....ValidationModels.Register import RegisterUser
from .....ValidationModels.Login import LoginByLP
from .....ValidationModels.Recovery import RecoverySetCode, Recovery
from .....ResponseModels.Register import (RegisterResponseFail, RegisterResponseSucces)

from ......database.tables import (authefication)
from .....tags import USER, EMAIL


@app.post('/api/admin/register', tags=[USER])
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
        return JSONResponse(status_code=403, content={'msg': f"{data.email} вже зареєстрований"})
    
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

    return JSONResponse(status_code=200, content={'token': token, 'user_data': t.parse_user_data(user._asdict())})


@app.post("/api/admin/login", tags=[USER])
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

        return JSONResponse(status_code=200, content={"token": token, 'user_data': t.parse_user_data(user._asdict())})
    
    return JSONResponse(status_code=403, content={"msg": f"{email} користувач відсутній в системі або хибний пароль"})


@app.post('/api/admin/set/recovery/code', tags=[USER, EMAIL])
async def set_recovery_code(data: RecoverySetCode) -> RegisterResponseFail:

    """
    <h1>Встановлення коду для відновлення</h1>
    <p>Метод створює код для відновлення паролю та надсилає його на пошту користувача яка вказана в тілі запиту</p>
    """

    email = data.email

    try: find_user = await db.async_get_where(authefication, exp=authefication.c.email == email,
                                              all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання емейлу для відновлення паролю.\n\nEmail: {email}\nError: {e}")
        return JSONResponse(status_code=400, content={"msg": "Помилка під час пошуку користувача"})
    
    if find_user is None:
        return JSONResponse(status_code=400, content={"msg": "Користувч відстуній в системі"})

    find_user = find_user["email"] 
    code = recovery.set_code()

    recovery[find_user] = code

    try:
        msg = f"""If you don't request code for recovery, ignore this mail.\nYour code for recovery: {code}"""
        send = await send_mail(find_user, "Restaurant QR-system recovery account", msg)
        return JSONResponse(status_code=200, content=send)

    except Exception as e:
        del recovery[find_user]
        logger.error(f"Помилка під час відправки email.\n\nEmail: {find_user}\nError: {e}")
        return JSONResponse(status_code=500, content={"msg": "Невідома помилка під час обробки транзакії"})


@app.post("/api/admin/recovery/code/check", tags=[USER])
async def recovery_code_check(data: Recovery) -> RegisterResponseFail:

    """
    <p>Метод перевіряє код який надіслав користувач та якщо код дійсний повертає стасус 200</p>
    """

    email, code = data.email, data.code

    try: find_user = await db.async_get_where(authefication, exp=authefication.c.email == email,
                                              all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання емейлу для відновлення паролю.\n\nEmail: {email}\nError: {e}")
        return JSONResponse(status_code=400, content={"msg": "Помилка під час пошуку користувача"})
    
    if find_user is None:
        return JSONResponse(status_code=400, content={"msg": "Користувч відстуній в системі"})
    
    find_user = find_user["email"] 

    if code == recovery[find_user]:
        del recovery[find_user]
        return JSONResponse(status_code=200, content={"msg": "Код дійсний."})
    
    return JSONResponse(status_code=403, content={"msg": "Введений код не дійсний"})