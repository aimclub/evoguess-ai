from typing import TYPE_CHECKING
from numpy.random import randint, RandomState

from typings.optional import Int

if TYPE_CHECKING:
    from core.model.point import PointSet


class Selection:
    slug = 'selection'

    def __init__(self, random_seed: Int = None):
        self.random_seed = random_seed or randint(2 ** 31 - 1)
        self.random_state = RandomState(seed=self.random_seed)

    def select(self, population: 'PointSet', size: int) -> 'PointSet':
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
