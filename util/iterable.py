from copy import copy
from math import ceil
from itertools import chain
from typing import Union, Callable, Iterable, Tuple, List, TypeVar

T = TypeVar('T', covariant=True)
Dimension = Union[int, Iterable]
Predicate = Union[Callable, Iterable]


def identity(_object: T) -> T:
    return _object


def to_oct(bits: Iterable[int]) -> int:
    return from_bin(bits, 8)


def concat(*iterables: Iterable[T]) -> List[T]:
    return list(chain(*iterables))


def to_bin(value: int, size: int) -> List[int]:
    return [1 if value & (1 << (size - 1 - i)) else 0 for i in range(size)]


def from_bin(bits: Iterable[int], size: int) -> int:
    return sum([1 << (size - i - 1) for i, bit in enumerate(bits) if bit])


def list_of(example: T, dimension: Dimension) -> List[T]:
    if hasattr(dimension, '__iter__'):
        return [copy(example) for _ in dimension]
    else:
        return [copy(example) for _ in range(dimension)]


def pick_by(iterable: Iterable[T], predicate: Predicate = identity) -> List[T]:
    if isinstance(predicate, Callable):
        return [item for item in iterable if predicate(item)]
    elif isinstance(predicate, Iterable):
        predicate = set(predicate)
        return [item for i, item in enumerate(iterable) if i in predicate]
    else:
        raise TypeError(
            f'unexpected predicate type: \'{type(predicate).__name__}\''
        )


def omit_by(iterable: Iterable[T], predicate: Predicate = identity) -> List[T]:
    if isinstance(predicate, Callable):
        return [item for item in iterable if not predicate(item)]
    elif isinstance(predicate, Iterable):
        return [item for i, item in enumerate(iterable) if i not in predicate]
    else:
        raise TypeError(
            f'unexpected predicate type: \'{type(predicate).__name__}\'')


def slice_by(sized: List[T], size: int) -> Iterable[List[T]]:
    for start in range(0, len(sized), size):
        yield sized[start:start + size]


def slice_into(sized: List[T], count: int) -> Iterable[List[T]]:
    return slice_by(sized, ceil(len(sized) / count))


def split_by(
        iterable: Iterable[T],
        predicate: Predicate = identity
) -> Tuple[List[T], List[T]]:
    left, right = [], []
    for i, item in enumerate(iterable):
        if isinstance(predicate, Callable):
            (left if predicate(item) else right).append(item)
        elif isinstance(predicate, Iterable):
            (left if i in predicate else right).append(item)
        else:
            raise TypeError(
                f'unexpected predicate type: \'{type(predicate).__name__}\'')

    return left, right
