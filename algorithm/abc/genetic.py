from typing import List, Iterable, Tuple, TYPE_CHECKING

from .evolution import Evolution
from ..module.mutation import Mutation
from ..module.selection import Selection
from ..module.crossover import Crossover

from typings.optional import Int
from util.iterable import slice_by, concat

if TYPE_CHECKING:
    from core.model.point import Vector
    from instance.module.variables import Backdoor


class Genetic(Evolution):
    tweak_size = 2

    def __init__(self, min_update_size: int, max_queue_size: Int,
                 mutation: Mutation, crossover: Crossover, selection: Selection):
        super().__init__(min_update_size, max_queue_size, mutation, selection)
        self.crossover = crossover

    def join(self, parents: 'Vector', offspring: 'Vector') -> 'Vector':
        raise NotImplementedError

    def tweak(self, selected: List['Backdoor']) -> List['Backdoor']:
        return concat(*map(self._apply, slice_by(selected, 2)))

    def _apply(self, individuals: Tuple['Backdoor']) -> Iterable['Backdoor']:
        if len(individuals) == 2:
            individuals = self.crossover.cross(*individuals)
        return map(self.mutation.mutate, individuals)

    def __info__(self):
        return {
            **super().__info__(),
            'crossover': self.crossover
        }


__all__ = [
    'Genetic'
]
