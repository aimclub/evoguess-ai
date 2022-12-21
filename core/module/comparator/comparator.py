from typing import Any, Dict


class Comparator:
    slug = None

    def compare(self, obj1: Any, obj2: Any) -> int:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Comparator'
]
