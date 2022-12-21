from typing import Any


class CoreCache:
    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key)

    def __setattr__(self, key: str, value: Any):
        self.__dict__[key] = value


CORE_CACHE = CoreCache()

__all__ = [
    'CORE_CACHE'
]
