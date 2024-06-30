from typing import TYPE_CHECKING

from ..selection import *
from typings.optional import Int

if TYPE_CHECKING:
    from core.model.point import PointSet


class Tournament(Selection):
    slug = 'selection:tournament'

    def __init__(self, rounds: int, random_seed: Int = None):
        self.rounds = rounds
        super().__init__(random_seed)

    def select(self, population: PointSet, size: int) -> PointSet:
        pass

    def __info__(self):
        return {
            **super().__info__(),
            'rounds': self.rounds
        }


__all__ = [
    'Tournament'
]
