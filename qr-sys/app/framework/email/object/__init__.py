from email.mime import text as t, multipart as m
import smtplib
import os

from ...celery.object import celery
from ....settings import (SENDER_EMAIL, SENDER_PASSWORD,
                          SMTP_PORT, SMTP_SERVER, DEBUG, logger)



EMAIL = SENDER_EMAIL if DEBUG else os.environ.get("SENDER_EMAIL") if "SENDER_EMAIL" in os.environ.keys() else None 
PASS = SENDER_PASSWORD if DEBUG else os.environ.get("SENDER_PASSWORD") if "SENDER_PASSWORD" in os.environ.keys() else None 
PORT = SMTP_PORT if DEBUG else os.environ.get("SMTP_PORT") if "SMTP_PORT" in os.environ.keys() else None 
SERVER = SMTP_SERVER if DEBUG else os.environ.get("SMTP_SERVER") if "SMTP_SERVER" in os.environ.keys() else None 

def setup_message(*args):
    e, s, b = args

    msg = m.MIMEMultipart()
    msg["Subject"] = s
    msg["From"] = EMAIL
    msg["To"] = e

    msg.attach(t.MIMEText(b, "plain"))

    return msg

@celery.task
def send_mail(email_to: str, theme: str, body: str) -> dict | Exception:
    try:
        msg = setup_message(email_to, theme, body)
        with smtplib.SMTP_SSL(host=SERVER, port=PORT) as smtp:
            smtp.login(EMAIL, PASS)
            smtp.sendmail(EMAIL, email_to, msg.as_bytes())

        return {"msg" : f"Повідомлення надіслано до {email_to}"}
    except Exception as e:
        logger.error(f"Помилка під час відправки емейлу\n\nFrom: {EMAIL} to {email_to}\nError: {e}")
        raise e