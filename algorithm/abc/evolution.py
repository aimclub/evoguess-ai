from math import ceil
from typing import List, TYPE_CHECKING

from .algorithm import Algorithm
from ..module.mutation import Mutation
from ..module.selection import Selection

from typings.optional import Int

if TYPE_CHECKING:
    from core.model.point import Vector, Point
    from instance.module.variables import Backdoor


class Evolution(Algorithm):
    tweak_size = 1

    def __init__(self, min_update_size: int, max_queue_size: Int,
                 mutation: Mutation, selection: Selection):
        super().__init__(min_update_size, max_queue_size)
        self.selection = selection
        self.mutation = mutation

    def update(self, vector: 'Vector', *points: 'Point') -> 'Vector':
        return self.join(vector, list(points))

    def join(self, parents: 'Vector', offspring: 'Vector') -> 'Vector':
        raise NotImplementedError

    def tweak(self, selected: List['Backdoor']) -> List['Backdoor']:
        return list(map(self.mutation.mutate, selected))

    def next(self, vector: 'Vector', count: int) -> List['Backdoor']:
        count = self.tweak_size * ceil(count / self.tweak_size)
        selected = self.selection.select(vector, count)
        return self.tweak([p.backdoor for p in selected])

    def __info__(self):
        return {
            **super().__info__(),
            'mutation': self.mutation,
            'selection': self.selection
        }


__all__ = [
    'Evolution'
]
