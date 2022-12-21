from itertools import chain
from typing import List, Optional
from numpy.random import RandomState

from ..module.encoding import Encoding
from ..module.variables.vars import Var, Supplements, compress
from ..module.variables import Variables, get_var_deps, get_var_bases


class InstanceVars:
    def __init__(
            self,
            dependent_vars: List[Var],
            propagation_vars: List[Var]
    ):
        self.dependent_vars = dependent_vars
        self.propagation_vars = propagation_vars

        self._var_deps = get_var_deps(propagation_vars)
        self._deps_bases = get_var_bases(self._var_deps)

    def get_propagation(self, state: RandomState) -> Supplements:
        _deps_values = {
            var: value for var, value in
            zip(self._var_deps, state.randint(0, self._deps_bases))
        }
        return compress(*(
            var.supplements(_deps_values) for var in self.propagation_vars
        ))

    def get_dependent(self, solution: List[int]) -> Supplements:
        _values = {abs(lit): 1 if lit > 0 else 0 for lit in solution}
        return compress(*(
            var.supplements(_values) for var in self.dependent_vars
        ))


class Instance:
    slug = 'instance'
    input_dependent = False

    def __init__(self, encoding: Encoding):
        self.encoding = encoding

    def get_propagation_vars(self) -> List[Var]:
        return []

    def get_dependent_vars(self, *args: Variables) -> List[Var]:
        return list(chain(*(arg.variables() for arg in args)))

    def get_instance_vars(self, *deps: Variables) -> Optional[InstanceVars]:
        dependent_vars = self.get_dependent_vars(*deps)
        # todo: zero check is needed?
        return InstanceVars(
            dependent_vars=dependent_vars,
            propagation_vars=self.get_propagation_vars(),
        ) if len(dependent_vars) > 0 else None

    def __str__(self):
        return f'{self.slug} of {self.encoding}'

    def __info__(self):
        return {
            'slug': self.slug,
            'encoding': self.encoding.__info__(),
        }


__all__ = [
    'Instance',
    'InstanceVars'
]
