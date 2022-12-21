from typing import Tuple
from numpy.random import randint, RandomState

from typings.optional import Int
from instance.module.variables import Backdoor


class Crossover:
    slug = 'crossover'

    def __init__(self, random_seed: Int = None):
        self.random_seed = random_seed or randint(2 ** 32 - 1)
        self.random_state = RandomState(seed=self.random_seed)

    def cross(self, ind1: Backdoor, ind2: Backdoor) -> Tuple[Backdoor, Backdoor]:
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
