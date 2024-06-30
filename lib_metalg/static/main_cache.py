from typing import Any


class MainCache:
    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key)

    def __setattr__(self, key: str, value: Any):
        self.__dict__[key] = value


MAIN_CACHE = MainCache()

__all__ = [
    'MAIN_CACHE'
]
