import threading
from typing import Any, Dict, NamedTuple
from concurrent.futures import Future, ThreadPoolExecutor

from core.model.point import Point

from lib_satprob.problem import Problem
from typings.searchable import Searchable


class SearchableCache(NamedTuple):
    estimated: Dict[Searchable, Point]
    estimating: Dict[Searchable, Future]


cache_lock = threading.Lock()
CACHE = SearchableCache({}, {})


def update_cache(point: Point):
    with cache_lock:
        searchable = point.searchable
        if searchable in CACHE.estimating:
            del CACHE.estimating[searchable]
        CACHE.estimated[searchable] = point

    return point


def get_future_with(
        point: Point
) -> Future:
    future = Future()
    future.set_result(point)
    return future


class Context(NamedTuple):
    problem: Problem
    executor: ThreadPoolExecutor


class Function:
    context = None
    caller_dict = {}

    def set_context(
            self,
            context: Context
    ) -> 'Function':
        self.context = context
        return self

    def evaluate(
            self,
            searchable: Searchable,
            caller: int = 0,
    ) -> Future:
        if searchable in CACHE.estimating:
            return CACHE.estimating[searchable]
        if searchable in CACHE.estimated:
            point = CACHE.estimated[searchable]
            return get_future_with(point)

        priority = self.caller_dict.get(caller, 0)
        self.caller_dict[caller] = priority + 1
        return self._evaluate(searchable, priority)

    def _evaluate(
            self,
            searchable: Searchable,
            priority: int = 0,
    ) -> Future:
        raise NotImplementedError

    __all__ = [
        'Function',
        # utility
        'update_cache'
    ]
