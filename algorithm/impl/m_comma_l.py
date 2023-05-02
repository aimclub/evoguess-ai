from ..abc import Evolution
from ..module.mutation import Mutation
from ..module.selection import Selection

from typings.optional import Int
from core.model.point import PointSet


class MuCommaLambda(Evolution):
    slug = 'evolution:comma'

    def __init__(self, mu_size: int, lambda_size: int, mutation: Mutation,
                 selection: Selection, max_queue_size: Int = None):
        self.mu_size, self.lambda_size = mu_size, lambda_size
        super().__init__(lambda_size, max_queue_size, mutation, selection)

    def join(self, parents: PointSet, offspring: PointSet) -> PointSet:
        return sorted(offspring)[:self.mu_size]

    def __info__(self):
        return {
            **super().__info__(),
            'mu_size': self.mu_size,
            'lambda_size': self.lambda_size
        }


__all__ = [
    'MuCommaLambda'
]
