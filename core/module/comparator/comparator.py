from typing import Any, Dict
from typings.ordered import Ordered


class Comparator:
    slug = None

    def compare(self, obj1: Ordered, obj2: Ordered) -> int:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Comparator'
]
