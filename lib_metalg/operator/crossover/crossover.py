from typing import Tuple
from numpy.random import randint, RandomState

from typings.optional import Int
from typings.searchable import Searchable


class Crossover:
    slug = 'crossover'

    def __init__(self, random_seed: Int = None):
        self.random_seed = random_seed or randint(2 ** 31)
        self.random_state = RandomState(seed=self.random_seed)

    def cross(self, ind1: Searchable, ind2: Searchable) -> Searchable:
        return self.cross2(ind1, ind2)[self.random_state.randint(2)]

    def cross2(self, ind1: Searchable, ind2: Searchable) -> Tuple[Searchable, Searchable]:
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'seed': self.random_seed
        }

    def __str__(self):
        return self.slug


__all__ = [
    'Crossover'
]
