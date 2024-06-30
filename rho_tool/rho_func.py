from time import time
from typing import List, NamedTuple

from lib_satprob.solver import _Solver
from lib_satprob.problem import Problem
from lib_satprob.variables.vars import Var

Task = List[int]


class RhoStats(NamedTuple):
    propagated: int
    easy_count: int
    rho_value: float
    hard_tasks: List[Task]


def _rho_func_tree(solver: _Solver, variables: List[Var]) -> RhoStats:
    count, easy_count, hard_tasks = 0, 0, [[]]
    for i, var in enumerate(variables):
        next_hard_tasks = []
        for hard_task in hard_tasks:
            for value in range(var.dim):
                count += 1
                assumption = hard_task + var.sub(value)
                report = solver.propagate((assumption, []))
                if report.status is False:
                    easy_pow = len(variables) - i - 1
                    easy_count += var.dim ** easy_pow
                else:
                    next_hard_tasks.append(assumption)

        hard_tasks = next_hard_tasks

    rho_value = easy_count / 2 ** len(variables)
    return RhoStats(count, easy_count, rho_value, hard_tasks)


class RhoCalc(NamedTuple):
    time: float
    value: float
    propagated: int
    easy_count: int
    hard_count: int
    rho_value: float


def rho_func_tree(problem: Problem, variables: List[Var]) -> RhoCalc:
    stamp, formula = time(), problem.encoding.get_formula()
    with problem.solver.get_instance(formula) as solver:
        count, easy_count, hard_tasks, rho_value = \
            _rho_func_tree(solver, variables)

    return RhoCalc(
        time=time() - stamp, hard_count=len(hard_tasks),
        easy_count=easy_count, value=1 - rho_value,
        rho_value=rho_value, propagated=count
    )


__all__ = [
    'rho_func_tree',
    '_rho_func_tree',
    # types
    'RhoCalc',
    'RhoStats'
]
