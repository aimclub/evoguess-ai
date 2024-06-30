from concurrent.futures import Future
from typing import List

from ._future import Single
from .function import _process_state, ProcessFunction

from ..func import rho_func_tree
from ..sampling import Sampling

from space.model import Backdoor
from core.model.point import Point
from lib_satprob.problem import Problem
from typings.searchable import Searchable
from core.module.comparator import MinValueMaxSize

COMPARATOR = MinValueMaxSize()


def hard_to_num(hard_task: List[int]) -> int:
    return sum([
        2 ** i if lit > 0 else 0 for i, lit in
        enumerate(sorted(hard_task, key=abs)[::-1])
    ])


def rho_fn(backdoor: Backdoor) -> Point:
    problem = _process_state.problem
    variables = backdoor.variables()
    calc = rho_func_tree(problem, variables)
    return Point(backdoor, COMPARATOR).set(
        hard=len(calc.hard_tasks), value=calc.value,
        hard_nums=list(map(hard_to_num, calc.hard_tasks))
    )


class FunctionRho(ProcessFunction):
    def __init__(
            self,
            problem: Problem,
            max_workers: int = None,
            sampling: Sampling = None,
    ):
        self._sampling = sampling
        super().__init__(
            problem,
            max_workers
        )

    def _evaluate(
            self,
            searchable: Searchable,
            priority: int = 0,
    ) -> Future:
        if not isinstance(searchable, Backdoor):
            raise TypeError("Defined only for backdoors")
        # return self._pool.submit(rho_fn, searchable)
        return Single(self._pool.submit(rho_fn, searchable))


__all__ = [
    'FunctionRho'
]
