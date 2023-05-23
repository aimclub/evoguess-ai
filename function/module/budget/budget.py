from typing import Tuple

from typings.optional import Str, Float

KeyLimit = Tuple[Str, Float]
UNLIMITED = ('', None)


class Budget:
    def value(self) -> float:
        raise NotImplementedError


__all__ = [
    'Budget',
    # types
    'KeyLimit',
    'UNLIMITED'
]
