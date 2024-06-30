from os import cpu_count
from typing import Any, List
from concurrent.futures import Future, ProcessPoolExecutor

from ..function import Function

from lib_satprob.problem import Problem
from typings.searchable import Searchable


class _ProcessState:
    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key)

    def __setattr__(self, key: str, value: Any):
        self.__dict__[key] = value


_process_state = _ProcessState()


def _pool_initializer(problem: Problem):
    _process_state.problem = problem


def _init_pool(
        problem: Problem,
        max_workers: int = None
) -> ProcessPoolExecutor:
    if max_workers is None:
        max_workers = cpu_count() or 1

    return ProcessPoolExecutor(
        initargs=(problem,),
        max_workers=max_workers,
        initializer=_pool_initializer,
    )


class ProcessFunction(Function):
    def __init__(
            self,
            problem: Problem,
            max_workers: int = None
    ):
        self._problem = problem
        self._pool = _init_pool(
            problem, max_workers
        )
        self.max_workers = \
            self._pool._max_workers

    def _evaluate(
            self,
            searchable: Searchable,
            priority: int = 0,
    ) -> Future:
        raise NotImplementedError


__all__ = [
    'ProcessFunction',
    # utility
    '_process_state'
]
