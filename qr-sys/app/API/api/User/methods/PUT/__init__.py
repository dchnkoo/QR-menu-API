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
    
    change_password = {"password": password}
    try: await db.async_update_data(authefication, exp=authefication.c.id == user_id,
                                    **change_password)
    except Exception as e:
        logger.error(f"Помилка під час зміни паролю користувача.\n\nId: {user_id}\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки транзакції")
    
    return JSONResponse(status_code=200, content={"msg": f"Пароль для користувача змінено"})