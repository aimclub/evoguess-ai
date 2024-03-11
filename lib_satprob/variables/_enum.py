from operator import itemgetter
from numpy.random import RandomState
from typing import List, Optional, Iterator, Callable

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
            self, from_nums: Optional[Iterator[int]] = None,
            with_random_state: Optional[RandomState] = None
    ) -> Iterator[Supplements]:
        dimension, power = self.dimension(), self.power()
        from_nums = from_nums if from_nums else range(0, power)
        # length = min(length or power - offset, power - offset)
        # assert offset >= 0 < length, 'Numbers must be positive!'

        shuffle = with_random_state and power <= self.permutation_limit
        sequence_fn = with_random_state.permutation if shuffle else range

        yield from map(self.substitute, map(
            get_num_to_values_fn(dimension), (
                number for index, number in
                enumerate(sequence_fn(power))
                if index in from_nums
            )
        ))

    __all__ = [
        'Enumerable'
    ]
