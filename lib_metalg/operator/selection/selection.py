from typing import List
from numpy.random import randint, RandomState

from core.model.point import Point
from typings.optional import Int


class Selection:
    slug = 'selection'

    def __init__(self, random_seed: Int = None):
        self.random_seed = random_seed or randint(2 ** 31)
        self.random_state = RandomState(seed=self.random_seed)

    def select(self, population: List[Point], size: int) -> List[Point]:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'seed': self.random_seed
        }


__all__ = [
    'Selection'
]
