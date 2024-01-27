from typing import Any
from ..JWTCache.cache_decorator.decorator import jwtcache, jwtgetcache


class JWTMetaData:

    @jwtgetcache
    def __init__(self) -> None:
        self._tokens = None

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_tokens':
            super().__setattr__(name, value)
        else:
            self._tokens[name] = value

    @jwtcache
    def __setitem__(self, key: str, value: Any) -> None:
        self._tokens[key] = value

    def __getattribute__(self, __name: str) -> Any:
        if __name == '_tokens':
            return object.__getattribute__(self, '_tokens')
        else:
            return super().__getattribute__(__name)

    def __getitem__(self, __name: str) -> Any:
        return self._tokens[__name]

    @jwtcache
    def __delitem__(self, __name: str) -> None:
        del self._tokens[__name]

    def __repr__(self) -> str:
        return f"<JWTMetaData: {self._tokens}>"