# from numpy import argsort
# from util.iterable import pick_by

from ..reducer import Reducer

from instance import Instance
# from function.module.solver import pysat
# from function.module.measure import Propagations
from instance.module.variables import Variables
# from instance.module.variables.vars import Index


class RhoSubset(Reducer):
    _indexes = None
    slug = 'reducer:rho_subset'

    def __init__(self, of_size: int):
        self.of_size = of_size

    def reduce(self, instance: Instance, variables: Variables) -> Variables:
        pass
        # if self._indexes is None:
        #     data, measure = instance.encoding.get_data(), Propagations()
        #     with pysat.Glucose3().use_incremental(data, measure) as solver:
        #         _indexes = argsort([0 if not isinstance(var, Index) else sum((
        #             solver.propagate(var.supplements({var: 0})[0], add_model=False).value,
        #             solver.propagate(var.supplements({var: 1})[0], add_model=False).value
        #         )) for var in variables])[::-1][:self.of_size]
        #
        # return Variables(from_vars=pick_by(variables.variables(), _indexes))


__all__ = [
    'RhoSubset'
]
