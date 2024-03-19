import time

from functools import partial
from typing import Any, List, Tuple, \
    TypeVar, Iterable, Callable, NamedTuple

R = TypeVar('R', covariant=True)


class Timed(NamedTuple):
    result: R
    time: float


def _timed(
        fn: Callable[..., R],
        *args: Any, **kwargs: Any
):
    stamp = time.time()
    return Timed(
        fn(*args, **kwargs),
        time.time() - stamp
    )


def timed(
        fn: Callable[..., R]
) -> Callable[..., Timed]:
    return partial(_timed, fn)


def untime(
        zipped: Iterable[Timed]
) -> Tuple[List[R], float]:
    time_sum, results = 0, []
    for result, _time in zipped:
        time_sum += _time
        results.append(result)
    return results, time_sum


__all__ = [
    'timed',
    'untime'
]
