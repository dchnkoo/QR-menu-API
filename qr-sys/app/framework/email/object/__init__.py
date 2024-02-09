from email.mime import text as t, multipart as m
from aiosmtplib import SMTP
import os

from ....settings import (SENDER_EMAIL, SENDER_PASSWORD,
                          SMTP_PORT, SMTP_SERVER, DEBUG, logger)


class email:

    def __init__(self) -> None:
        self.sender = SENDER_EMAIL if DEBUG else os.environ.get("SENDER_EMAIL") if "SENDER_EMAIL" in os.environ.keys() else None 
        self.password = SENDER_PASSWORD if DEBUG else os.environ.get("SENDER_PASSWORD") if "SENDER_PASSWORD" in os.environ.keys() else None 
        self.port = SMTP_PORT if DEBUG else os.environ.get("SMTP_PORT") if "SMTP_PORT" in os.environ.keys() else None 
        self.server = SMTP_SERVER if DEBUG else os.environ.get("SMTP_SERVER") if "SMTP_SERVER" in os.environ.keys() else None 

    def setup_message(self, *args):
        e, s, b = args

        msg = m.MIMEMultipart()
        msg["Subject"] = s
        msg["From"] = self.sender
        msg["To"] = e

        msg.attach(t.MIMEText(b, "plain"))

        return msg

    async def __call__(self, email_to: str, theme: str, body: str) -> dict | Exception:
        try:
            msg = self.setup_message(email_to, theme, body)
            async with SMTP(hostname=self.server, port=self.port, start_tls=False) as smtp:
                await smtp.starttls()
                await smtp.login(self.sender, self.password)
                await smtp.sendmail(self.sender, email_to, msg.as_bytes())

            return {"msg" : f"Повідомлення надіслано до {email_to}"}
        except Exception as e:
            logger.error(f"Помилка під час відправки емейлу\n\nFrom: {self.sender} to {email_to}\nError: {e}")
            raise e