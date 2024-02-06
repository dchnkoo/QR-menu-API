from ......framework import app, jwt_validation, db, logger
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Register import RegisterResponseFail
from ......database.tables import authefication
from ...tags.tags import USER


@app.delete('/api/admin/delete/session/user', tags=[USER], dependencies=[Depends(jwt_validation)])
async def delete_user_from_session():
    """
    <h1>Вихід користувача з системи</h1>

    <p>Якщо потрібно вийти з аккаунту користувача потрібно відправити DELETE
    запит на цей url та обов'язково повинен бути токен в cookie. В іншому випадку
    буде помилка.</p>
    """

@app.delete('/api/admin/delete/user', tags=[USER])
async def delete_user(hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:
    try: await db.async_delete_data(authefication, exp=authefication.c.hashf == hashf)
    except Exception as e:
        logger.error(f"Помилка під час видалення користувача\n\nhashf: {hashf}\nError: {e}")
        return JSONResponse(status_code=500, content={"msg": "Невідома помилка під час виконання операції"})
    
    return JSONResponse(status_code=200, content={"msg": "Користувача видаленно з системи"})