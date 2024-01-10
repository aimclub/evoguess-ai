from typing import Any, List, Dict, Optional

from lib_satprob.variables import Supplements
from lib_satprob.variables.vars import VarMap, Var

from .interval import Interval
from typings.searchable import Searchable


class Partition(Searchable):
    slug = 'searchable:partition'

    def __init__(
            self, length: int,
            interval: Interval
    ):
        super().__init__(length=length)
        self._interval = interval

    def power(self) -> int:
        return self._interval.power()

    def dimension(self) -> List[int]:
        return self._interval.dimension()

    def variables(self) -> List[Var]:
        return self._interval.variables()

    def substitute(self, using_values: Optional[List[int]] = None,
                   using_var_map: Optional[VarMap] = None) -> Supplements:
        return self._interval.substitute(using_values, using_var_map)

    def __len__(self) -> int:
        return len(self._interval)

    def __str__(self) -> str:
        return ''.join(map(str, self._vector))

    def __hash__(self) -> int:
        return hash(tuple(self._vector))

    def __repr__(self) -> str:
        return f'[{str(self)}]({sum(self._vector)})'

    def __copy__(self) -> 'Partition':
        return Partition(self._length, self._interval)

    def __eq__(self, other: 'Partition') -> bool:
        return str(self) == str(other)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'interval': self._interval.__config__()
        }

__all__ = [
    'Partition'
]