from numpy.random import RandomState
from typing import Any, List, Dict, Union, Optional

from .solver import Solver, Report
from .encoding import Encoding, CNF, WCNF
from .variables.vars import Var, VarMap
from .variables import Indexes, Variables, Enumerable


class CommentSet:
    def __init__(self, leading: str = None):
        self.leading = leading

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

        assert (input_set and output_set) or \
               (not input_set and not output_set), \
            'Set both (input and output) sets or neither'

    def resolve(self, decomposition: Optional[Enumerable] = None,
                with_random_state: Optional[RandomState] = None,
                with_output_values: Optional[List[int]] = None,
                with_output_var_map: Optional[VarMap] = None,
                with_input_values: Optional[List[int]] = None,
                with_input_var_map: Optional[VarMap] = None) -> Report:
        formula, supplements = self.encoding.get_formula(), ([], [])
        if self.input_set and (with_input_values or with_input_var_map):
            with_output_var_map = self.process_output_var_map(
                None, with_input_values, with_input_var_map
            )
        if self.output_set and (with_output_values or with_output_var_map):
            supplements = self.input_set.substitute(
                with_output_values, with_output_var_map
            )

        if decomposition is None:
            return self.solver.solve(formula, supplements)

        state, stats_sum = with_random_state, {'count': 0}
        for supplements in decomposition.enumerate(with_random_state=state):
            status, stats, model = self.solver.solve(formula, supplements)
            for key in set(stats_sum.keys()).union(stats.keys()):
                stats_sum[key] = stats_sum.get(key, 0) + (
                    1 if key == 'count' else stats.get(key, 0)
                )
            print(stats_sum)
            # if status: return Report(status, stats_sum, model)
        else:
            return Report(False, stats_sum, None)

    def evaluate(self, decomposition: Enumerable, sample_length: int,
                 with_random_state: Optional[RandomState] = None) -> Report:
        # todo: add realisation
        pass

    def process_output_var_map(
            self, with_random_state: Optional[RandomState] = None,
            from_input_values: Optional[List[int]] = None,
            from_input_var_map: Optional[VarMap] = None
    ) -> VarMap:
        assert self.input_set, 'Input set not presented!'
        if not (from_input_values or from_input_var_map):
            dimension = self.input_set.dimension()
            random_state = with_random_state or RandomState()
            from_input_values = random_state.randint(0, dimension)

        # todo: optimize formula solving
        formula = self.encoding.get_formula()
        input_sups = self.input_set.substitute(
            from_input_values, from_input_var_map
        )
        return {
            abs(literal): 1 if literal > 0 else 0 for literal in
            self.solver.propagate(formula, input_sups).model
        }

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'encoding': self.encoding.__config__(),
            'input_set': self.input_set.__config__(),
            'output_set': self.output_set.__config__()
        }


class SatProblem(Problem):
    slug = 'problem:sat'

    def __init__(
            self, solver: Solver, encoding: CNF,
            input_set: InputSet = None, output_set: OutputSet = None
    ):
        super().__init__(solver, encoding, input_set, output_set)


class MaxSatProblem(Problem):
    slug = 'problem:max-sat'

    def __init__(
            self, solver: Solver, encoding: WCNF,
            input_set: InputSet = None, output_set: OutputSet = None
    ):
        super().__init__(solver, encoding, input_set, output_set)


__all__ = [
    'Problem',
    'SatProblem',
    'MaxSatProblem',
    # types
    'CommentSet',
]
