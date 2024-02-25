from ....database.db.models import sync, _async

from ....settings import DOMAIN, DEBUG, TABLES_PER_PAGE, QR_LOGO_HEIGHT, QR_LOGO_WIDTH, LOGO_OVRL, logger
from ....database.tables import tables

from ...image.object import image

from PIL import Image
import pyqrcode, os


class QR(image):

    def setup_logo_for_qr(self, logo: str, bg_rgb: tuple[int]) -> Image:
        lg = self.make_round(
            self.image_to_base64(
                self.resize_image(
                    self.str_to_base64(logo), QR_LOGO_WIDTH, QR_LOGO_HEIGHT
                )
            )
        )

        logo_bg = self.make_rounded_image(bg_rgb, LOGO_OVRL)

        coordinates = self.get_center_coordinates(lg, logo_bg)

        logo_bg.paste(lg, coordinates, lg)

        return self.image_to_base64(logo_bg)

    def paste_logo_in_qr(self, logo: bytes, QR: bytes):
        lg = self.open_bytes_image(logo)
        qr = self.open_bytes_image(QR)

        lg = lg.convert("RGBA")
        qr = qr.convert("RGBA")

        coordinates = self.get_center_coordinates(lg, qr)

        qr.paste(lg, coordinates, lg)

        return self.image_to_base64(qr)


    def _qr(self, restaurant: str, id: int, table: int, *args) -> str:
        domain = DOMAIN if DEBUG else os.environ.get('QR_DOMAIN')
        url = f"{domain}/menu/{restaurant}?id={id}&table={table}"
        
        logo, bg, fill = args

        qr = pyqrcode.QRCode(url)
        qr = self.str_to_base64(qr.png_as_base64_str(scale=10, quiet_zone=2,
                                                     module_color=fill, background=bg))
        
        if logo:
            qr = self.paste_logo_in_qr(logo, qr)
        
        return self.base64_to_str(qr), url


    def generate(self, restaurant: str, id: int, tables_: int, *args) -> None:
        db = sync.sync_db()

        logo, bg_rgb, fill = args

        if logo:
            logo = self.setup_logo_for_qr(logo, bg_rgb)


        tables_count = db.get_where(tables, exp=tables.c.restaurant_id == id, 
                                    all_=False, count=True, to_dict=True)

        start = (tables_count[1] + 1) if tables_count else 1

        for i in range(start, (start  + tables_)):
            qr, url = self._qr(restaurant, id, i, logo, bg_rgb, fill)


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