from typing import Tuple

from ..crossover import *

from typings.optional import Int
from typings.searchable import Searchable


class Uniform(Crossover):
    slug = 'crossover:uniform'

    def __init__(self, swap_prob: float = 0.5, random_seed: Int = None):
        self.swap_prob = swap_prob
        super().__init__(random_seed)

    def cross2(self, ind1: Searchable, ind2: Searchable) -> Tuple[Searchable, Searchable]:
        vector1, vector2 = ind1.get_vector(), ind2.get_vector()

        # todo: use _distribution from tool funcs
        distribution = self.random_state.rand(len(vector1))
        for i, value in enumerate(distribution):
            if self.swap_prob >= value:
                vector1[i], vector2[i] = vector2[i], vector1[i]

        return ind1.make_copy(vector1), ind2.make_copy(vector2)

    def __info__(self):
        return {
            **super().__info__(),
            'swap_prob': self.swap_prob
        }


__all__ = [
    'Uniform'
]
