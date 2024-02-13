from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Email import EmailMsg

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ......framework import app, send_mail, logger
from .....tags import EMAIL


@app.post("/api/admin/send_email", tags=[EMAIL])
async def send_email(data: EmailMsg) -> RegisterResponseFail:
    try:
        send_mail.delay(data.email_to, data.theme, data.body)
        return JSONResponse(status_code=200, content={"msg": "Повідомлення надіслано"})
    except Exception as e:
        logger.error(f"Помидка під час обробки функції send_mail\nError: {e}")
        raise HTTPException(status_code=400, detail="Помилка під час обробки транзакції")