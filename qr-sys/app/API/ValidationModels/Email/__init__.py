from pydantic import BaseModel, Field


class EmailMsg(BaseModel):
    email_to: str
    theme: str = Field(..., description="Тема листа")
    body: str = Field(..., description="Тіло листа")