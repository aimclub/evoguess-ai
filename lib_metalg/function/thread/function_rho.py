from concurrent.futures import Future

from ...point import Point
from ..func import rho_func_tree
from ..sampling import Sampling
from .function import ThreadFunction
from ..function import update_cache

from space.model import Backdoor

from lib_satprob.problem import Problem
from typings.searchable import Searchable
from core.module.comparator import MinValueMaxSize

COMPARATOR = MinValueMaxSize()


def rho_fn(problem: Problem, backdoor: Backdoor) -> Point:
    calc = rho_func_tree(problem, backdoor.variables())
    point = Point(backdoor, COMPARATOR).set(**calc._asdict())
    return update_cache(point)


class FunctionRho(ThreadFunction):
    estimated = {}
    estimating = {}
    caller_dict = {}

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

        return self._pool.submit(
            rho_fn, self._problem, searchable
        )


__all__ = [
    'FunctionRho'
]
