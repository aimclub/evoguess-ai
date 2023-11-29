from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.module.comparator import Comparator


class Ordered:
    def __init__(self, comparator: 'Comparator'):
        self.comparator = comparator

    def compare(self, other: 'Ordered') -> int:
        return self.comparator.compare(self, other)

    def __lt__(self, other: 'Ordered') -> bool:
        return self.compare(other) < 0

    def __gt__(self, other: 'Ordered') -> bool:
        return self.compare(other) > 0

    def __eq__(self, other: 'Ordered') -> bool:
        return self.compare(other) == 0

    def __le__(self, other: 'Ordered') -> bool:
        return self.compare(other) <= 0

    def __ge__(self, other: 'Ordered') -> bool:
        return self.compare(other) >= 0


__all__ = [
    'Ordered'
]
