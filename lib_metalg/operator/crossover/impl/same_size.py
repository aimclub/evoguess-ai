from typing import Tuple

from ..crossover import *

from typings.optional import Int
from typings.searchable import Searchable


class SameSize(Crossover):
    slug = 'crossover:same_size'

    def __init__(self, size: int, random_seed: Int = None):
        self.size = size
        self.swap_prob = 1. / self.size
        super().__init__(random_seed)

    def cross2(self, ind1: Searchable, ind2: Searchable) -> Tuple[Searchable, Searchable]:
        vector1, vector2 = ind1.get_vector(), ind2.get_vector()

        indexes1 = [i for i, bit in enumerate(vector1) if bit]
        indexes2 = [i for i, bit in enumerate(vector2) if bit]

        size = min(len(indexes1), len(indexes2))
        distribution = self.random_state.rand(size)
        for i, value in enumerate(distribution):
            if self.swap_prob >= value:
                vector1[indexes1[i]], vector2[indexes2[i]] =\
                    vector2[indexes2[i]], vector1[indexes1[i]]

        return ind1.make_copy(vector1), ind2.make_copy(vector2)


__all__ = [
    'SameSize'
]
