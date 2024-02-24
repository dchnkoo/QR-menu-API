import hashlib
from ...settings import logger

from typing import ByteString

from PIL import Image
from io import BytesIO
import base64



class trash:
    """Цей обьект для мусорних методів в цьому додатку"""

    def get_hash(self, string: str) -> str:
        """Перетворює str в hash"""
        h = hashlib.sha256(string.encode()).hexdigest()
        logger.info(f"{h[:10]} hash created")
        return h
    
    def parse_user_data(self, data: dict) -> dict:
        """Парсить обьєкт щоб прибрати з нього конфіденціїні дані"""
        return {k: v for k, v in data.items() if k not in ['password', 'hashf', 'token'] and v is not None}
    
    @staticmethod
    def check_images_size(image: ByteString, width: str, height: str):
        """Метод перевіряє розмір зображення, аргумент повинен бути закодований в base64 та мати тип данних str"""
        try:
            image_decode = base64.b64decode(image)
            image = Image.open(BytesIO(image_decode))
        except Exception as e:
            logger.error(f"Помилка під час обробки логотипу\nError: {e}")
            return False, 400, "Неправильний формат логотипу, він повинен бути як base64 str"
        
        if (sz := image.size) and sz[0] > width or sz[1] > height:
            return False, 413, f"Логотип перевищує задані параметри {width}x{height}"
        
        return True, 200, ""