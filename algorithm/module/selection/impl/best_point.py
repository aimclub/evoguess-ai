from typing import TYPE_CHECKING

from ..selection import *
from typings.optional import Int

if TYPE_CHECKING:
    from core.model.point import Vector


class BestPoint(Selection):
    slug = 'selection:best-point'

    def __init__(self, best_count: int, random_seed: Int = None):
        self.best_count = best_count
        super().__init__(random_seed)

    def select(self, population: 'Vector', size: int) -> 'Vector':
        mx = min(self.best_count, len(population))
        return [
            sorted(population)[i % mx] for i in
            self.random_state.permutation(size)
        ]

    def __info__(self):
        return {
            **super().__info__(),
            'best_count': self.best_count
        }


__all__ = [
    'BestPoint'
]
