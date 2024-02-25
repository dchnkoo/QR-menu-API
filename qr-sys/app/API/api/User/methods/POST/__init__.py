from ......framework import app, db, t, jwt, recovery, send_mail, logger

from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .....ValidationModels.Recovery import RecoverySetCode, Recovery
from .....ResponseModels.Register import RegisterResponseFail
from .....ResponseModels.Recovery import ResponseCheckRecovery
from .....ValidationModels.Register import RegisterUser
from .....ValidationModels.Login import LoginByLP

from ......database.tables import (authefication)
from .....tags import USER, EMAIL


@app.post('/api/admin/register', tags=[USER])
async def register(data: RegisterUser) -> (RegisterResponseFail):

    if await db.async_get_where(authefication, exp=authefication.c.email == data.email, all_=False):
        raise HTTPException(status_code=403, detail=f"{data.email} вже зареєстрований")
    
    hashf = t.get_hash(data.email + data.password)
    password = t.get_hash(data.password)

    get_data = data.model_dump()
    get_data['hashf'] = hashf
    get_data['password'] = password

    time = get_data.pop('time')
    user = await db.async_insert_data(authefication, **get_data)

    playload, date, seconds = jwt.get_playload(user[0], user[2], **{time['type']: time['number']})
    token = jwt.get_token(**playload)
    jwt.set(token, user[1], seconds)

    response = JSONResponse(status_code=200, content={"msg": "Користувача зарєстровано"})
    response.set_cookie(key="token", value=token, expires=date, httponly=True, secure=True, samesite="none")
    return response


@app.post("/api/admin/login", tags=[USER])
async def login(data: LoginByLP) -> RegisterResponseFail:

    email, password, time_type, time = data.email, t.get_hash(data.password), data.time.type, data.time.number
    user = await db.async_get_where(authefication, exp=authefication.c.email == email, all_=False, to_dict=True)

    if user is None:
        raise HTTPException(status_code=403, detail=f"{email} користувач відсутній")

    if password != user.get("password"):
        raise HTTPException(status_code=403, detail=f"Хибний пароль для {email}")

    # Генеруємо новий токен, зберігаємо та повертаємо дані
    playload, date, seconds = jwt.get_playload(user.get("id"), user.get("email"), **{time_type: time})
    token = jwt.get_token(**playload)
    jwt.set(token, user.get("hashf"), seconds)

    response = JSONResponse(status_code=200, content={"msg": "Вхід в систему успішний"})
    response.set_cookie(key="token", value=token, expires=date, httponly=True, secure=True, samesite="none")

    return response
    


@app.post('/api/admin/set/recovery/code', tags=[USER, EMAIL])
async def set_recovery_code(data: RecoverySetCode) -> RegisterResponseFail:

    """
    <h1>Встановлення коду для відновлення</h1>
    <p>Метод створює код для відновлення паролю та надсилає його на пошту користувача яка вказана в тілі запиту</p>
    """

    email = data.email
    code = recovery.set_code()

    recovery[email] = code

    try:
        msg = f"""If you don't request code for recovery, ignore this mail.\nYour code for recovery: {code}"""
        send_mail.delay(email, "Restaurant QR-system recovery account", msg)
        return JSONResponse(status_code=200, content={"msg": "Плвідомлення надіслано"})

    except Exception as e:
        del recovery[email]
        logger.error(f"Помилка під час відправки email.\n\nEmail: {email}\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки транзакії")


@app.post("/api/admin/recovery/code/check", tags=[USER])
async def recovery_code_check(data: Recovery) -> (ResponseCheckRecovery | RegisterResponseFail):

    """
    <p>Метод перевіряє код який надіслав користувач та якщо код дійсний повертає стасус 200</p>
    """

    email, id, code = *data.email, data.code 

    if code == recovery[email]:
        del recovery[email]
        return JSONResponse(status_code=200, content={"msg": "Код дійсний.", "id": id})
    
    raise HTTPException(status_code=403, detail="Введений код не дійсний")