from typing import Any
from random import choice

from ....redis import get_redis_connection
from .....settings import REDIS_DB, DEBUG, RECOVERY_TIME
import os


code = get_redis_connection(REDIS_DB + 3 if DEBUG else int(os.environ.get("REDIS_DB")) + 3)

class recovery_codes:

    def set_code(self) -> str:
        return "".join([str(choice(range(10))) for _ in range(6)])

    def __setitem__(self, key: Any, value: Any) -> None:
        code.set(key, value)
        code.expire(key, RECOVERY_TIME)

    def __delitem__(self, key: Any) -> None:
        code.delete(key)

    def __getitem__(self, key: Any) -> Any:
        return code.get(key).decode()