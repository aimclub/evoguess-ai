import time

from functools import partial
from typing import Callable, Any, TypeVar, NamedTuple

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


__all__ = [
    'timed'
]
