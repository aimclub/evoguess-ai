from numpy import argsort
from typing import Any, Dict, Optional

from ..space import Space

from util.iterable import pick_by
from typings.optional import Str

from instance.impl import Instance
from function.module.solver import pysat
from function.module.measure import Propagations
from instance.module.variables import Backdoor, Variables, Indexes, Mask


class RhoSubset(Space):
    slug = 'space:rho_subset'
    _subset = None

    def __init__(self, of_size: int, variables: Variables,
                 by_string: Str = None, by_mask: Optional[Mask] = None):
        super().__init__(by_string, by_mask)
        self.variables = variables
        self.of_size = of_size

    # noinspection PyProtectedMember
    def get_backdoor(self, instance: Instance) -> Backdoor:
        if not self._subset:
            data, measure = instance.encoding.get_data(), Propagations()
            with pysat.Glucose3().use_incremental(data, measure) as solver:
                variable_weights = [sum((
                    solver.propagate(var.supplements({var: 0})[0], add_model=False).value,
                    solver.propagate(var.supplements({var: 1})[0], add_model=False).value
                )) for var in self.variables]
                indexes = argsort(variable_weights)[::-1][:self.of_size]
                self._subset = pick_by(self.variables.variables(), indexes)

        return Backdoor(from_vars=self._subset)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'of_size': self.of_size,
            'by_mask': self.by_mask,
            'by_string': self.by_string,
            'variables': self.variables.__config__(),
        }


__all__ = [
    'RhoSubset'
]
