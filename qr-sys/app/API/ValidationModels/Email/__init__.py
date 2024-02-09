from pydantic import BaseModel


class EmailMsg(BaseModel):
    email_to: str
    theme: str
    body: str