from numpy.random import randint, RandomState

from typings.optional import Int
from typings.searchable import Searchable


class Mutation:
    slug = 'mutation'

    def __init__(self, random_seed: Int = None):
        self.random_seed = random_seed or randint(2 ** 32 - 1)
        self.random_state = RandomState(seed=self.random_seed)

    def _distribution(self, min_prob, length):
        while True:
            distribution = self.random_state.rand(length)
            if min_prob <= 0 or min_prob > min(distribution):
                return distribution

    def mutate(self, individual: Searchable) -> Searchable:
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'seed': self.random_seed
        }

    def __str__(self):
        return self.slug


__all__ = [
    'Mutation'
]
