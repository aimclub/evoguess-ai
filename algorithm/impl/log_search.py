from typing import TYPE_CHECKING

from ..abc import Evolution
from ..module.mutation import Mutation
from ..module.selection import Selection

from typings.optional import Int

if TYPE_CHECKING:
    from core.model.point import PointSet


class LogSearch(Evolution):
    slug = 'evolution:log_search'

    def __init__(self, population_size: int, mutation: Mutation, selection: Selection,
                 min_update_size: int = 1, max_queue_size: Int = None):
        self.population_size = population_size
        min_update_size = min(min_update_size, population_size)
        super().__init__(min_update_size, max_queue_size, mutation, selection)

    def join(self, parents: 'PointSet', offspring: 'PointSet') -> 'PointSet':
        return sorted([*parents, *offspring])[:self.population_size]

    def __info__(self):
        return {
            **super().__info__(),
            'mutation': self.mutation,
            'selection': self.selection,
            'population_size': self.population_size,
        }


__all__ = [
    'LogSearch'
]
