from typing import Any

from ..abc import Logger


class NoneLogger(Logger):
    slug = 'logger:optimize'

    def __init__(self):
        super().__init__(None)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def meta(self, *args: Any, **kwargs: Any) -> Logger:
        pass

    def write(self, *args: Any, **kwargs: Any) -> Logger:
        pass

    def config(self, *args: Any, **kwargs: Any) -> Logger:
        pass


__all__ = [
    'NoneLogger'
]
