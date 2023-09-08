from numpy.random import RandomState
from typing import Any, List, Dict, Union, Optional

from ._utility import Supplements, combine
from .encoding import Encoding, CNF, WCNF
from .variables import Indexes, Variables
from .variables.vars import Var, \
    VarMap, get_var_deps, get_var_dims
from .solver import Solver, _Solver


class CommentSet:
    def __init__(self, leading: str = None):
        pass

    def variables(self) -> List[Var]:
        pass


InputSet = Optional[Union[
    Indexes, CommentSet
]]

OutputSet = Optional[Union[
    Variables, CommentSet
]]


class Problem:
    slug = 'problem'

    def __init__(
            self,
            solver: Solver,
            encoding: Encoding,
            input_set: Indexes = None,
            output_set: Variables = None
    ):
        self.solver = solver
        self.encoding = encoding
        self.input_set = input_set
        self.output_set = output_set

    def _get_input_vars(self) -> List[Var]:
        return self.input_set.variables()

    def _get_output_vars(self) -> List[Var]:
        return self.output_set.variables()

    def get_input_supplements(
            self, from_values: Optional[List[int]] = None,
            from_random_state: Optional[RandomState] = None
    ) -> Supplements:
        # todo: optimize
        input_vars = self._get_input_vars()
        var_deps = get_var_deps(input_vars)

        values = from_values if from_values else \
            from_random_state.randint(0, get_var_dims(var_deps))

        var_map = {var: value for var, value in zip(var_deps, values)}
        return combine(*(var.supplements(var_map) for var in input_vars))

    def get_output_supplements(self, var_map: VarMap) -> Supplements:
        return combine(*(
            var.supplements(var_map) for var in self._get_output_vars()
        ))

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'encoding': self.encoding.__config__(),
            'input_set': self.input_set.__config__(),
            'output_set': self.output_set.__config__()
        }


class Sat(Problem):
    slug = 'problem:sat'

    def __init__(
            self, solver: Solver, encoding: CNF,
            input_set: InputSet = None, output_set: OutputSet = None
    ):
        super().__init__(solver, encoding, input_set, output_set)


class MaxSat(Problem):
    slug = 'problem:max-sat'

    def __init__(
            self, solver: Solver, encoding: WCNF,
            input_set: InputSet = None, output_set: OutputSet = None
    ):
        super().__init__(solver, encoding, input_set, output_set)


__all__ = [
    'Sat',
    'MaxSat',
    'Problem',
    # types
    'CommentSet'
]
