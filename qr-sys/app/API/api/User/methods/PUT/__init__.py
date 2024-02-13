from ......framework import app, db, t, logger
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .....ValidationModels.Recovery import RecoveryPassword
from .....ResponseModels.Register import RegisterResponseFail

from ......database.tables import authefication
from .....tags import USER


@app.put("/api/admin/recovery/password", tags=[USER])
async def recovery_password(data: RecoveryPassword) -> RegisterResponseFail:

    """
    <h1>Встановлює новий пароль для користувача</h1>
    """

    user_id, password = data.id, t.get_hash(data.password)

    try: find_user = await db.async_get_where(authefication, exp=authefication.c.id == user_id,
                                              all_=False, to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання емейлу для відновлення паролю.\n\nEmail: {email}\nError: {e}")
        raise HTTPException(status_code=400, detail="Помилка під час пошуку користувача")
    
    if find_user is None:
        raise HTTPException(status_code=400, detail="Користувч відстуній в системі")
    
    find_user = find_user["id"]

    change_password = {"password": password}
    try: await db.async_update_data(authefication, exp=authefication.c.id == find_user,
                                    **change_password)
    except Exception as e:
        logger.error(f"Помилка під час зміни паролю користувача.\n\nEmail: {find_user}\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки транзакції")
    
    return JSONResponse(status_code=200, content={"msg": f"Пароль для користувача змінено"})