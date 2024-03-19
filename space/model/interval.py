from math import log2, floor
from sys import getrecursionlimit, setrecursionlimit
from typing import Any, List, Dict, Tuple, Optional

from lib_satprob.variables import Indexes, \
    Assumptions, Constraints, Supplements, prod
from lib_satprob.variables.vars import Var, VarMap

from utility.iterable import to_bin, split_by, from_bin
from typings.searchable import Searchable, Vector


def _geq(lower: Assumptions) -> Constraints:
    if len(lower) == 0: return []
    return [[lower[0]], *_geq(lower[1:])] if lower[0] > 0 \
        else [[-lower[0], *clause] for clause in _geq(lower[1:])]


def _leq(upper: Assumptions) -> Constraints:
    if len(upper) == 0: return []
    return [[upper[0]], *_leq(upper[1:])] if upper[0] < 0 \
        else [[-upper[0], *clause] for clause in _leq(upper[1:])]


def _both(lower: Assumptions, upper: Assumptions) -> Constraints:
    if len(lower) == 0 or len(upper) == 0: return []
    assert abs(lower[0]) == abs(upper[0])

    if lower[0] > 0:  # 1 1
        assert upper[0] > 0
        return [[lower[0]], *_both(lower[1:], upper[1:])]
    elif upper[0] < 0:  # 0 0
        assert lower[0] < 0
        return [[upper[0]], *_both(lower[1:], upper[1:])]
    else:  # 0 1
        return [*_geq(lower), *_leq(upper)]


class Interval(Searchable):
    def __init__(self, indexes: Indexes):
        super().__init__(length=len(indexes))
        self._indexes = indexes

        self._int_size = None
        self._int_power = None
        self._int_oversize = None

    def power(self) -> int:
        if self._int_power is None:
            self._int_power = 1 + from_bin(
                self._vector, self._length
            )
        return self._int_power

    def dimension(self) -> List[int]:
        return self._indexes.dimension()

    def variables(self) -> List[Var]:
        return self._indexes.variables()

    def substitute(self, using_values: Optional[List[int]] = None,
                   using_var_map: Optional[VarMap] = None) -> Supplements:
        values = using_values if using_var_map is None else [
            using_var_map[_var] for _var in self._indexes
        ]
        # todo: replace recursive method by iterative
        if getrecursionlimit() < len(self._vector) + 100:
            setrecursionlimit(2048)

        number = from_bin(values, self._length)
        length, remainder = self._get_size()
        if number >= self._int_oversize:
            offset = (number - self._int_oversize) % length
            lower = int(number - offset)
            upper = lower + length - 1
        else:
            offset = (number % (length + 1))
            lower = int(number - offset)
            upper = lower + length

        # print('n, l, p:', number, lower, upper)
        # print('d, r, -:', length, remainder, self._length)
        constraints, one_lit_clauses = split_by(_both(
            self._indexes.substitute(to_bin(lower, self._length))[0],
            self._indexes.substitute(to_bin(upper, self._length))[0]
        ), lambda x: len(x) > 1)
        return [clause[0] for clause in one_lit_clauses], constraints

    def _get_size(self) -> Tuple[int, int]:
        if self._int_size is None:
            self._int_size = length, remainder = divmod(
                prod(self.dimension()), self.power()
            )
            self._int_oversize = remainder * (length + 1)
        return self._int_size

    def _set_vector(self, vector: Vector) -> 'Interval':
        self._int_size = None
        self._int_power = None
        self._int_oversize = None
        return super()._set_vector(vector)

    def __len__(self) -> int:
        return floor(log2(self._get_size()[0]))

    def __str__(self) -> str:
        return f'0-{self._get_size()[0]}'

    def __hash__(self) -> int:
        return hash(tuple(self._vector))

    def __repr__(self) -> str:
        return f'[{str(self)}]({self.power()})'

    def __copy__(self) -> 'Interval':
        return Interval(indexes=self._indexes)

    def __eq__(self, other: 'Interval') -> bool:
        # todo: more effective __eq__
        return str(self) == str(other)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'indexes': self._indexes.__config__()
        }


__all__ = [
    'Interval'
]
