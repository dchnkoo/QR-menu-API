from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Email import EmailMsg

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
        return JSONResponse(status_code=400, content={"msg": "Помилка під час обробки транзакції"})