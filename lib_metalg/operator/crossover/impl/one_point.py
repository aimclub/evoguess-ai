from typing import Tuple

from ..crossover import *

from typings.searchable import Searchable


class OnePoint(Crossover):
    slug = 'crossover:one-point'

    def cross2(self, ind1: Searchable, ind2: Searchable) -> Tuple[Searchable, Searchable]:
        vector1, vector2 = ind1.get_vector(), ind2.get_vector()

        a = self.random_state.randint(len(vector1))
        b = self.random_state.randint(2) * len(vector1)
        for i in range(min(a, b), max(a, b)):
            vector1[i], vector2[i] = vector2[i], vector1[i]

        return ind1.make_copy(vector1), ind2.make_copy(vector2)


__all__ = [
    'OnePoint'
]
