from ..selection import *

from typings.optional import Int
from core.model.point import Vector


class Tournament(Selection):
    slug = 'selection:tournament'

    def __init__(self, rounds: int, random_seed: Int = None):
        self.rounds = rounds
        super().__init__(random_seed)

    def select(self, vector: Vector, size: int) -> Vector:
        pass

    def __info__(self):
        return {
            **super().__info__(),
            'rounds': self.rounds
        }


__all__ = [
    'Tournament'
]
