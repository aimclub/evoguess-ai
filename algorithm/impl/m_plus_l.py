from numpy import argsort

from ..abc import Evolution
from ..module.mutation import Mutation
from ..module.selection import Selection

from typings.optional import Int
from core.model.point import Vector
from util.iterable import pick_by, omit_by


class MuPlusLambda(Evolution):
    slug = 'evolution:plus'

    def __init__(self, mu_size: int, lambda_size: int, mutation: Mutation,
                 selection: Selection, min_update_size: int = 1, max_queue_size: Int = None):
        min_update_size = min(min_update_size, lambda_size)
        self.mu_size, self.lambda_size = mu_size, lambda_size
        super().__init__(min_update_size, max_queue_size, mutation, selection)

    def join(self, parents: Vector, offspring: Vector) -> Vector:
        mu_indexes = argsort(parents)[:self.mu_size]
        additional_size = max(0, self.lambda_size - len(offspring))
        additional_lmbda = omit_by(parents, mu_indexes)[:additional_size]
        return [*pick_by(parents, mu_indexes), *offspring, *additional_lmbda]

    def __info__(self):
        return {
            **super().__info__(),
            'mu_size': self.mu_size,
            'lambda_size': self.lambda_size
        }


__all__ = [
    'MuPlusLambda'
]
