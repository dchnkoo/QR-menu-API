from ....database.db.models import sync, _async
from io import BytesIO

from ....settings import DOMAIN, TABLES_PER_PAGE, logger
from ....database.tables import tables

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
        db = sync.sync_db()
    
        for i in range(1, tables_ + 1):
            qr, url = self._qr(restaurant, id, i)

            data = {
                'menu_link': url,
                'qr': qr,
                'table_number': i,
                'restaurant_id': id
            }

            db.insert_data(tables, get_data=False, **data)

    def threads(self, func, *args):
        import multiprocessing

        th = multiprocessing.Process(target=func, args=args)
        th.daemon = True 
        th.start()


    def delete_all(self, restaurant_id: int) -> None:
        db = sync.sync_db()

        try: db.delete_data(tables, exp=tables.c.restaurant_id == restaurant_id)
        except Exception as e:
            logger.error(f"Помилка під час видалення данних про столи\n\nError: {e}")


    async def delete_table(self, restaurant_id: int, table_number: int) -> None:
        db = _async.async_db()

        try: await db.async_delete_data(tables, and__=(tables.c.restaurant_id == restaurant_id,
                                      tables.c.table_number == table_number))
        except Exception as e:
            logger.error(f"Помилка під час видалення данних про столи\n\nError: {e}")


    async def get_tables(self, restaurant_id: int, page: int = 1) -> list[dict]:
        from fastapi.responses import JSONResponse
        
        db = _async.async_db()

        offset = (page - 1) * TABLES_PER_PAGE

        try: data, total = await db.async_get_where(tables, exp=tables.c.restaurant_id == restaurant_id,
                     count=True, offset=offset, limit=TABLES_PER_PAGE, to_dict=True)
        except Exception as e:
            logger.error(f"Помилка під час отримання данних про столи\n\nError: {e}")
            return JSONResponse(status_code=500, content={"msg": "Невідома помилка під час обробки запиту"})

        total_pages = (total + TABLES_PER_PAGE - 1) // TABLES_PER_PAGE

        return JSONResponse(status_code=200, content={"data": data, 'total_pages': total_pages, 'page': page})