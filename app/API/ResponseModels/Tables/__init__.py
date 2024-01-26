from pydantic import BaseModel
from typing import List


class GetTablesData(BaseModel):
    id: int
    menu_link: str
    qr: str
    table_number: int
    restaurant_id: int


class GetTablesResponse(BaseModel):
    data: List[GetTablesData]
    total_pages: int
    page: int