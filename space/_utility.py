from numpy import argsort
from util.polyfill import prod
from util.iterable import pick_by

from lib_satprob.problem import Problem
from lib_satprob.variables import Variables


def rho_subset(
        problem: Problem, variables: Variables,
        of_size: int = None, by_weight: int = None
) -> Variables:
    formula = problem.encoding.get_formula()
    with problem.solver.get_instance(formula, use_timer=False) as solver:
        print('no assumptions:', solver.propagate(([], [])).stats)
        _weights = [prod((
            solver.propagate(var.substitute({var: 0})).stats['propagations'],
            solver.propagate(var.substitute({var: 1})).stats['propagations'],
        )) for var in variables]
        print('weights:', set(_weights))
        _indexes = argsort(_weights)[::-1][:of_size] if by_weight is None else [
            _i for _i, _weight in enumerate(_weights) if _weight >= by_weight
        ]
        print(len(_indexes))

    return Variables(from_vars=pick_by(variables.variables(), _indexes))
