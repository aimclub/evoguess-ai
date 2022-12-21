from copy import copy
from functools import reduce
from itertools import islice
from typing import Union, Callable, Iterable, Tuple, List, Any, TypeVar

T = TypeVar('T', covariant=True)
Dimension = Union[int, Iterable]
Predicate = Union[Callable, Iterable]


def identity(_object: T) -> T:
    return _object


def concat(*iterables: Iterable[T]) -> List[T]:
    return reduce(lambda x, y: x.extend(y) or x, iterables, [])


def to_oct(bits: Iterable[int]) -> int:
    return sum([1 << (7 - i) for i, bit in enumerate(bits) if bit])


def to_bin(value: int, size: int) -> List[int]:
    return [1 if value & (1 << (size - 1 - i)) else 0 for i in range(size)]


def list_of(example: T, dimension: Dimension) -> List[T]:
    if hasattr(dimension, '__iter__'):
        return [copy(example) for _ in dimension]
    else:
        return [copy(example) for _ in range(dimension)]


def pick_by(iterable: Iterable[T], predicate: Predicate = identity) -> List[T]:
    if isinstance(predicate, Callable):
        return [item for item in iterable if predicate(item)]
    elif isinstance(predicate, Iterable):
        return [item for i, item in enumerate(iterable) if i in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def omit_by(iterable: Iterable[T], predicate: Predicate = identity) -> List[T]:
    if isinstance(predicate, Callable):
        return [item for item in iterable if not predicate(item)]
    elif isinstance(predicate, Iterable):
        return [item for i, item in enumerate(iterable) if i not in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def slice_by(iterable: Iterable[T], size: int) -> Iterable[Tuple[T]]:
    iterator = iter(iterable)
    # todo: refactor this
    return iter(lambda: tuple(islice(iterator, size)), ())


def split_by(iterable: Iterable[T], predicate: Predicate = identity) -> Tuple[List[T], List[T]]:
    left, right = [], []
    for i, item in enumerate(iterable):
        if isinstance(predicate, Callable):
            (left if predicate(item) else right).append(item)
        elif isinstance(predicate, Iterable):
            (left if i in predicate else right).append(item)
        else:
            raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')

    return left, right
