from typing import List, Iterable, Optional, Callable
from numpy.random import RandomState

from ._utility import Supplements


def get_num_to_values_fn(dimension: List[int]) -> Callable:
    reversed_dimension = dimension[::-1]

    def _num_to_values(number: int) -> List[int]:
        substitution = []
        for base in reversed_dimension:
            number, value = divmod(number, base)
            substitution.insert(0, value)
        return substitution

    return _num_to_values


class Enumerable:
    permutation_limit = 2 ** 20

    def power(self) -> int:
        raise NotImplementedError

    def dimension(self) -> List[int]:
        raise NotImplementedError

    def substitute(self, using_values: List[int]) -> Supplements:
        raise NotImplementedError

    def enumerate(
            self, offset: int = 0, length: Optional[int] = None,
            with_random_state: Optional[RandomState] = None,
    ) -> Iterable[Supplements]:
        dimension, power = self.dimension(), self.power()
        length = min(length or power - offset, power - offset)
        assert offset >= 0 < length, 'Numbers must be positive!'

        sequence_fn = range if power > self.permutation_limit \
            else (with_random_state or RandomState()).permutation

        yield from map(self.substitute, map(
            get_num_to_values_fn(dimension),
            sequence_fn(power)[offset:offset + length]
        ))


__all__ = [
    'Enumerable'
]
