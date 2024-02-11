from pydantic import BaseModel


class ResponseCheckRecovery(BaseModel):
    msg: str
    id: int