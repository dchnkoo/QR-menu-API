from ...redis import get_redis_connection
from ....settings import REDIS_DB, DEBUG

from typing import Any
import os


re = get_redis_connection(REDIS_DB if DEBUG else os.environ.get("REDIS_DB"))

class JWTMetaData:

    def __init__(self) -> None:
        self._tokens = {}

    def __setitem__(self, key: str, value: Any) -> None:
        re.set(key, value)

    def __getitem__(self, __name: str) -> Any:
        hashf = re.get(__name)

        return hashf.decode()

    def __delitem__(self, __name: str) -> None:
        re.delete(__name)