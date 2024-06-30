from time import time
from typing import List, NamedTuple

from lib_satprob.problem import Problem
from lib_satprob.variables import combine
from lib_satprob.variables.vars import Var


class RhoCalc(NamedTuple):
    hard: int
    easy: int
    time: float
    value: float
    rho_value: float
    propagated: int
    hard_tasks: List


# todo: make recursive
def _rho_fn_tree():
    pass


def rho_func_tree(problem: Problem, variables: List[Var]) -> RhoCalc:
    stamp, formula = time(), problem.encoding.get_formula()
    with problem.solver.get_instance(formula) as incremental:
        count, easy_count, hard_tasks = 0, 0, [[]]
        for i, var in enumerate(variables):
            next_hard_tasks = []
            for hard_task in hard_tasks:
                for value in range(var.dim):
                    count += 1
                    assumption = hard_task + var.sub(value)
                    report = incremental.propagate((assumption, []))
                    if report.status is False:
                        easy_pow = len(variables) - i - 1
                        easy_count += var.dim ** easy_pow
                    else:
                        next_hard_tasks.append(assumption)

            hard_tasks = next_hard_tasks

        hard_count = len(hard_tasks)
        power = easy_count + hard_count
        rho_value = easy_count / power

    return RhoCalc(
        hard=hard_count,
        easy=easy_count,
        time=time() - stamp,
        value=1 - rho_value,
        rho_value=rho_value,
        propagated=count,
        hard_tasks=hard_tasks,
    )


__all__ = [
    'rho_func_tree',
    # types
    'RhoCalc'
]
