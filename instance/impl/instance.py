from itertools import chain
from typing import List, Optional
from numpy.random import RandomState

from ..module.encoding import Encoding
from ..module.variables.vars import Var, get_var_deps, get_var_dims

from typings.searchable import Searchable, Supplements, combine


class InstanceVars:
    def __init__(
            self,
            searchable: Optional[Searchable],
            dependent_vars: List[Var],
            propagation_vars: List[Var],
    ):
        self.searchable = searchable
        self.dependent_vars = dependent_vars
        self.propagation_vars = propagation_vars

        self._var_deps = get_var_deps(propagation_vars)
        self._deps_bases = list(get_var_dims(self._var_deps))

    def get_propagation(self, state: RandomState) -> Supplements:
        _deps_values = {
            var: value for var, value in
            zip(self._var_deps, state.randint(0, self._deps_bases))
        }
        return combine(*(
            var.supplements(_deps_values) for var in self.propagation_vars
        ))

    def get_dependent(self, solution: List[int]) -> Supplements:
        var_map = {abs(lit): 1 if lit > 0 else 0 for lit in solution}
        searchable_sups = ([], []) if self.searchable is None else \
            self.searchable.substitute(with_var_map=var_map)
        return combine(searchable_sups, *(
            var.supplements(var_map) for var in self.dependent_vars
        ))


class Instance:
    slug = 'instance'
    input_dependent = False

    def __init__(self, encoding: Encoding):
        self.encoding = encoding

    def get_dependent_vars(self) -> List[Var]:
        return []

    def get_propagation_vars(self) -> List[Var]:
        return []

    def get_instance_vars(self, searchable: Optional[Searchable] = None) -> InstanceVars:
        return InstanceVars(
            searchable=searchable,
            dependent_vars=self.get_dependent_vars(),
            propagation_vars=self.get_propagation_vars(),
        )

    def __str__(self):
        return f'{self.slug} of {self.encoding}'

    # def __info__(self):
    #     return {
    #         'slug': self.slug,
    #     }


__all__ = [
    'Instance',
    'InstanceVars'
]
