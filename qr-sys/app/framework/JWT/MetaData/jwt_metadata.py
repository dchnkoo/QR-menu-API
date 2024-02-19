from ...redis import get_redis_connection
from ....settings import REDIS_DB, DEBUG

from functools import singledispatchmethod
from typing import Any, List
import os


re = get_redis_connection(REDIS_DB if DEBUG else os.environ.get("REDIS_DB"))

class JWTMetaData(dict):

    def clear(self):
        re.flushdb()

    def copy(self) -> Exception:
        """Can't be copied"""
        raise Exception(f"{self.__class__.__name__} can't be copied")
    
    def keys(self) -> List:
        """return List[...]"""
        return re.keys()
    
    def set(self, __key: Any, __value: Any) -> None:
        self.__setitem__(__key, __value)

    def setdefault(self):
        raise Exception("Can't set default got JWTMetaData")

    def delete(self, token) -> None:
        self.__delitem__(token)

    def pop(self, key: Any) -> Any:
        """
        return List[key: str, value: str]
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
    
