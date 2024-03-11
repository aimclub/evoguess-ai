from typing import List, Optional, Any

from typings.ordered import Ordered
from typings.searchable import Searchable
from core.module.comparator import Comparator


class Point(Ordered):
    def __init__(self, searchable: Searchable, comparator: Comparator):
        self.estimation = {}
        self.searchable = searchable
        super().__init__(comparator)

    def estimated(self) -> bool:
        return self.value() is not None

    def value(self) -> Optional[float]:
        return self.estimation.get('value')

    def get(self, key: str) -> Any:
        return self.estimation.get(key)

    def set(self, **estimation: Any) -> 'Point':
        if 'value' in self.estimation:
            raise Exception('Estimation already set')
        self.estimation.update(estimation)
        return self

    def __len__(self):
        return len(self.searchable)

    def __str__(self):
        return f'{repr(self.searchable)} by {self.value():.7g}'


PointSet = List[Point]

__all__ = [
    'Point',
    'PointSet',
]
