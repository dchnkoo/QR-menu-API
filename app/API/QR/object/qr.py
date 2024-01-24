from ....database.db.db_model import DB
from io import BytesIO
import threading

from ....settings import DOMAIN
from ....database.tables import tables, restaurant

import base64
import qrcode


class QR:

    def _qr(self, restaurant: str, id: int, table: int) -> str:
        buffer = BytesIO()
        url = f"{DOMAIN}/menu/{restaurant}?id={id}&table={table}"

        qr = qrcode.make(url)
        qr.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode(), url

    def generate(self, restaurant: str, id: int, tables_: int) -> None:
        db = DB()
        for i in range(1, tables_ + 1):
            qr, url = self._qr(restaurant, id, i)

            data = {
                'menu_link': url,
                'qr': qr,
                'table_number': i,
                'restaurant_id': id
            }

            db.insert_data(tables, **data)

    def threads(self, func, *args):

        th = threading.Thread(target=func, args=args)
        th.daemon = True
        th.start()

        return True
    
    def delete_all(self, restaurant_id: int) -> None:
        db = DB()

        data = db.get_where(tables, exp=tables.c.restaurant_id == restaurant_id)

        for i in range(len(data)):
            db.delete_data(tables, exp=tables.c.id == data[i][0])

    def delete_table(self, restaurant_id: int, table_number: int) -> None:
        db = DB()

        db.delete_data(tables, and__=(tables.c.restaurant_id == restaurant_id,
                                      tables.c.table_number == table_number))
        