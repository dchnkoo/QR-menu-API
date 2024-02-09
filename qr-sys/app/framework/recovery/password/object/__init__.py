from typing import Any
from random import choice


class recovery_codes:

    def __init__(self) -> None:
        self.code = {}

    def set_code(self) -> str:
        return "".join([str(choice(range(10))) for _ in range(6)])

    def __setitem__(self, key: Any, value: Any) -> None:
        self.code[key] = value

    def __delitem__(self, key: Any) -> None:
        del self.code[key]

    def __getitem__(self, key: Any) -> Any:
        return self.code[key]