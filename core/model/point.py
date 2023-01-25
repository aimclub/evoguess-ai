from typing import List, Optional

from typings.ordered import Ordered
from typings.optional import Primitive
from core.module.comparator import Comparator
from instance.module.variables import Backdoor


class Point(Ordered):
    def __init__(self, backdoor: Backdoor, comparator: Comparator):
        self.estimation = {}
        self.backdoor = backdoor
        super().__init__(comparator)

    def estimated(self) -> bool:
        return self.value() is not None

    def value(self) -> Optional[float]:
        return self.estimation.get('value')

    def set(self, **estimation: Primitive) -> 'Point':
        if 'value' in self.estimation:
            raise Exception('Estimation already set')
        self.estimation.update(estimation)
        return self

    def __len__(self):
        return len(self.backdoor)

    def __str__(self):
        return f'{repr(self.backdoor)} by {self.value():.7g}'


Vector = List[Point]

__all__ = [
    'Point',
    'Vector',
]
