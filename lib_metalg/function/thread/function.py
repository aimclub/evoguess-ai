from os import cpu_count
from typing import Any, List
from concurrent.futures import Future, ThreadPoolExecutor

from ..function import Function

from lib_satprob.problem import Problem
from typings.searchable import Searchable


def _init_pool(
        max_workers: int = None
) -> ThreadPoolExecutor:
    if max_workers is None:
        max_workers = cpu_count() or 1

    return ThreadPoolExecutor(
        max_workers=max_workers
    )


class ThreadFunction(Function):
    def __init__(
            self,
            problem: Problem,
            max_workers: int = None
    ):
        self._problem = problem
        self._pool = _init_pool(
            max_workers
        )

    def _evaluate(
            self,
            searchable: Searchable,
            priority: int = 0,
    ) -> Future:
        raise NotImplementedError


__all__ = [
    'ThreadFunction',
]
