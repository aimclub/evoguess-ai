from itertools import compress
from util.polyfill import prod
from typing import Optional, Iterator, List, Dict, Any

from pysatmc.variables import Variables
from pysatmc.variables.vars import Var, \
    VarMap, get_var_dims, get_var_sups

from typings.searchable import Vector, Searchable, Supplements


class Backdoor(Searchable):
    slug = 'searchable:backdoor'

    def __init__(self, variables: Variables):
        super().__init__(length=len(variables))
        self._variables = variables

        self._var_deps = None
        self._var_bases = None
        self._var_state = None

    def power(self) -> int:
        return prod(self.dimension())

    def dimension(self) -> List[int]:
        if not self._var_bases:
            self._var_bases = list(get_var_dims(self.variables()))
        return self._var_bases

    def variables(self) -> List[Var]:
        if not self._var_state:
            self._var_state = list(compress(self._variables, self._vector))
        return self._var_state

    def substitute(self, using_values: Optional[List[int]] = None,
                   using_var_map: Optional[VarMap] = None) -> Supplements:
        return get_var_sups(self.variables(), using_var_map, using_values)

    def _set_vector(self, vector: Vector) -> 'Backdoor':
        self._var_deps = None
        self._var_state = None
        self._var_bases = None
        return super()._set_vector(vector)

    def __copy__(self) -> 'Backdoor':
        return Backdoor(self._variables)

    def __len__(self) -> int:
        return len(self.variables())

    def __str__(self) -> str:
        return ' '.join(map(str, self.variables()))

    def __repr__(self) -> str:
        return f'[{str(self)}]({len(self)})'

    def __hash__(self) -> int:
        return hash(tuple(self._vector))

    def __iter__(self) -> Iterator[Var]:
        return iter(self.variables())

    def __contains__(self, item: Var) -> bool:
        return item in self.variables()

    def __eq__(self, other: 'Backdoor') -> bool:
        # todo: more effective __eq__
        return str(self) == str(other)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'variables': self._variables.__config__()
        }


__all__ = [
    'Backdoor'
]
