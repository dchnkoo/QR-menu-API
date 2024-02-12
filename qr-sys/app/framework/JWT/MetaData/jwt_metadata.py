from typing import Any
from ...redis import re


class JWTMetaData:

    def __init__(self) -> None:
        self._tokens = {}

    def __setitem__(self, key: str, value: Any) -> None:
        re.set(key, value)

    def __getitem__(self, __name: str) -> Any:
        hashf = re.get(__name)

        return hashf.decode("utf-8")

    def __delitem__(self, __name: str) -> None:
        re.delete(__name)