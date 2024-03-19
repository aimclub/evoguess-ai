from typing import Tuple
from numpy import argsort

from utility.polyfill import prod
from utility.iterable import pick_by, to_bin

from lib_satprob.problem import Problem, SatProblem
from lib_satprob.encoding import WCNF, is_sat_formula
from lib_satprob.variables import Variables, Range

from .impl import PartitionSet
from .model import Interval


def rho_subset(
        problem: Problem, variables: Variables,
        of_size: int = None, by_weight: int = None
) -> Variables:
    formula = problem.encoding.get_formula()
    with problem.solver.get_instance(formula, use_timer=False) as solver:
        solver.propagate(([], []))
        _weights = [prod((
            solver.propagate(var.substitute({var: 0})).stats['propagations'],
            solver.propagate(var.substitute({var: 1})).stats['propagations'],
        )) for var in variables]
        _indexes = argsort(_weights)[::-1][:of_size] if by_weight is None else [
            _i for _i, _weight in enumerate(_weights) if _weight >= by_weight
        ]

    return Variables(from_vars=pick_by(variables.variables(), _indexes))


def init_partition(
        problem: Problem, weaken: int
) -> Tuple[SatProblem, PartitionSet]:
    formula = problem.encoding.get_formula()

    if problem.input_set is not None:
        interval = Interval(problem.input_set)
    else:
        interval = Interval(Range(length=formula.nv))

    if isinstance(problem, SatProblem):
        if is_sat_formula(formula):
            by_vector = [1] * len(formula.clauses)
        else:
            raise TypeError(f'Unknown formula {type(formula)}')
    elif isinstance(problem.encoding, WCNF):
        by_vector = [
            *([1] * len(formula.hard)),
            *([0] * len(formula.soft))
        ]
        problem = SatProblem(
            solver=problem.solver,
            encoding=problem.encoding.unweighted(),
            input_set=problem.input_set,
            output_set=problem.output_set,
        )
    else:
        raise TypeError(f'Unknown problem {type(problem)}')

    return problem, PartitionSet(
        by_vector=by_vector,
        length=len(by_vector),
        interval=interval._set_vector(
            to_bin(weaken, len(interval._vector))
        )
    )


__all__ = [
    'rho_subset',
    'init_partition',
]
