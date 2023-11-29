from numpy import argsort
from util.iterable import pick_by

from lib_satprob.problem import Problem
from lib_satprob.variables import Variables


def rho_subset(
        problem: Problem, variables: Variables, of_size: int
) -> Variables:
    formula = problem.encoding.get_formula()
    with problem.solver.get_instance(formula, use_timer=False) as solver:
        _indexes = argsort([sum((
            solver.propagate(var.substitute({var: 0})).stats['propagations'],
            solver.propagate(var.substitute({var: 1})).stats['propagations'],
        )) for var in variables])[::-1][:of_size]

    return Variables(from_vars=pick_by(variables.variables(), _indexes))
