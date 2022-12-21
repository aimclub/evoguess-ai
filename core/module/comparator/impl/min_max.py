from numpy import sign
from typing import Dict, Any, TYPE_CHECKING

from ..comparator import Comparator

if TYPE_CHECKING:
    from core.model.point import Point


class MinValueMaxSize(Comparator):
    slug = 'comparator:min_max'

    def compare(self, obj1: 'Point', obj2: 'Point'):
        try:
            v1, v2 = obj1.value(), obj2.value()
            difference = int(sign(v1 - v2))
        except (TypeError, ValueError):
            difference = 0
        return difference or len(obj2) - len(obj1)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug
        }


__all__ = [
    'MinValueMaxSize'
]
