from numpy import argsort

from ..abc import Genetic
from ..module.mutation import Mutation
from ..module.crossover import Crossover
from ..module.selection import Selection

from typings.optional import Int
from core.model.point import PointSet
from utility.iterable import pick_by, omit_by


class Elitism(Genetic):
    slug = 'genetic:elitism'

    def __init__(self, population_size: int, elites_count: int, mutation: Mutation,
                 crossover: Crossover, selection: Selection, min_update_size: int = 1,
                 max_queue_size: Int = None):
        min_update_size = min(min_update_size, population_size)
        self.elites_count, self.population_size = elites_count, population_size
        super().__init__(min_update_size, max_queue_size, mutation, crossover, selection)

    def join(self, parents: PointSet, offspring: PointSet) -> PointSet:
        # todo: fix same points in elites
        elite_indexes = argsort(parents)[:self.elites_count]
        additional_size = max(0, self.population_size - len(offspring))
        additional_parents = omit_by(parents, elite_indexes)[:additional_size]
        return [*pick_by(parents, elite_indexes), *offspring, *additional_parents]

    def __info__(self):
        return {
            **super().__info__(),
            'elites_count': self.elites_count,
            'population_size': self.population_size,
        }


__all__ = [
    'Elitism'
]
