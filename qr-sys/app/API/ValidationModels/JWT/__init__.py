from pydantic import BaseModel


class JWTliveTime(BaseModel):
    type: str = 'days'
    number: float = 1.0


class JWT(BaseModel):
    token: str