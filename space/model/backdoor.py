from itertools import compress
from util.polyfill import prod
from typing import Optional, Iterator, List, Dict, Any

from instance.module.variables import Variables, Var
from instance.module.variables.vars import get_var_dims
from typings.searchable import Vector, Searchable, Supplements, combine


class Backdoor(Searchable):
    slug = 'searchable:backdoor'

    def __init__(self, variables: Variables):
        super().__init__(length=len(variables))
        self._variables = variables

        self._var_deps = None
        self._var_bases = None
        self._var_state = None
        # self._deps_bases = None

    def power(self) -> int:
        return prod(self.dimension())

    def dimension(self) -> List[int]:
        if not self._var_bases:
            self._var_bases = list(get_var_dims(self.dependents()))
        return self._var_bases

    def dependents(self) -> List[Var]:
        # todo: rename this or get_var_deps
        if not self._var_state:
            self._var_state = list(compress(self._variables, self._vector))
        return self._var_state

    def substitute(
            self,
            with_var_map: Optional[Dict[int, bool]] = None,
            with_substitution: Optional[List[bool]] = None,
    ) -> Supplements:
        var_map = {
            _var: value for _var, value in
            zip(self.dependents(), with_substitution)
        } if with_substitution else with_var_map
        return combine(*(_var.supplements(var_map) for _var in self.dependents()))

    def _set_vector(self, vector: Vector) -> 'Backdoor':
        self._var_deps = None
        self._var_state = None
        self._var_bases = None
        # self._deps_bases = None
        return super()._set_vector(vector)

    def __copy__(self) -> 'Backdoor':
        return Backdoor(self._variables)

    def __len__(self) -> int:
        return len(self.dependents())

    def __str__(self) -> str:
        return ' '.join(map(str, self.dependents()))

    def __repr__(self) -> str:
        return f'[{str(self)}]({len(self)})'

    def __hash__(self) -> int:
        return hash(tuple(self.dependents()))

    def __iter__(self) -> Iterator[Var]:
        return iter(self.dependents())

    def __contains__(self, item: Var) -> bool:
        return item in self.dependents()

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
