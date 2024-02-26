from ...redis import get_redis_connection
from ....settings import REDIS_DB

from typing import Any, List
import os


re = get_redis_connection(os.environ.get("REDIS_DB", REDIS_DB))

class JWTMetaData(dict):

    def clear(self):
        """Видалення всіх данних з поточної БД"""
        re.flushdb()

    def copy(self) -> Exception:
        """Can't be copied"""
        raise Exception(f"{self.__class__.__name__} can't be copied")
    
    def keys(self) -> List:
        """Отримання всіх ключів"""
        return re.keys()
    
    def set(self, __key: Any, __value: Any, expire: int = None) -> None:
        """Збереження токену до БД та встановлення часу життя якщо expire != None"""
        self.__setitem__(__key, __value)
        if expire:
            re.expire(__key, expire)

    def setdefault(self):
        """В цьому обьєкті неможливо встановити дефолтне значення"""
        raise Exception("Can't set default got JWTMetaData")

    def delete(self, token) -> None:
        self.__delitem__(token)

    def pop(self, key: Any) -> Any:
        """
        Видаляє ключ з БД та повертає його значення
        """
        value = self.__getitem__(key)
        self.__delitem__(key)
        return value

    def get(self, key: Any) -> Any:
        return self.__getitem__(key)

    def __len__(self) -> int:
        return re.dbsize()
    
    def __setitem__(self, key: Any, value: Any) -> None:
        re.set(key, value)

    def __getitem__(self, __name: Any) -> Any:
        return re.get(__name)

    def __delitem__(self, __name: Any) -> None:
        return re.delete(__name)
    
