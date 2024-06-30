from typing import Any, Callable, List

from ..function import update_cache
from concurrent.futures import Future, wait
from concurrent.futures._base import RUNNING, FINISHED

from core.model.point import Point

Aggregator = Callable[
    [List[Future]],
    Point
]


class _Condition:
    def __init__(self, futures):
        self._futures = futures

    def acquire(self):
        for future in self._futures:
            future._condition.acquire()

    def __enter__(self):
        for future in self._futures:
            future._condition.acquire()

    def release(self):
        for future in self._futures:
            future._condition.release()

    def __exit__(self, *args):
        for future in self._futures:
            future._condition.release()


class Single(Future):
    def __init__(self, future: Future):
        self._future = future

    def __getattr__(self, name: str) -> Any:
        if name in ['result', '__hash__']:
            return super().__getattribute__(name)
        return self._future.__getattribute__(name)

    def result(self, timeout=None) -> Point:
        point = self._future.result(timeout)
        return update_cache(point)

    def __hash__(self) -> int:
        return self._future.__hash__()


class Multiple(Future):
    def __init__(
            self,
            futures: List[Future],
            aggregator: Aggregator,
    ):
        self._futures = set(futures)
        self._aggregator = aggregator

        self._waiters = []
        self._finished = []
        self._result = None
        self._state = RUNNING
        for future in self._futures:
            future.add_done_callback(
                self.done_callback
            )

    def done_callback(self, future: Future):
        self._finished.append(future)
        count = len(self._finished)
        # todo: double call trouble
        if len(self._futures) == count:
            self._result = self._aggregator(
                self._finished
            )
            update_cache(self._result)
            self._state = FINISHED
            for waiter in self._waiters:
                waiter.add_result(self)

    def __getattribute__(self, name: str):
        if name == '_condition':
            return _Condition(self._futures)
        return super().__getattribute__(name)

    def result(self, timeout=None):
        d, nd = wait([self], timeout)
        if self._state == FINISHED:
            return self._result
        else:
            raise TimeoutError()


__all__ = [
    'Single',
    'Multiple',
    # types
    'Aggregator'
]
