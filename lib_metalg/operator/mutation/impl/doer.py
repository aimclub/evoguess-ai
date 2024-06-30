from math import pow

from ..mutation import Mutation

from typings.optional import Int
from typings.searchable import Searchable


class Doer(Mutation):
    slug = 'mutation:doer'

    def __init__(self, beta: int = 3, random_seed: Int = None):
        self.beta = beta
        super().__init__(random_seed)

    def __get_alpha(self, size: int) -> int:
        bound = size // 2 + 1
        if bound < 3:
            return 1

        ll, p, rr = 0., self.random_state.rand(), 0.
        c = sum(1. / pow(i, self.beta) for i in range(1, bound))
        for k in range(1, bound):
            ll = rr
            rr += (1. / (c * pow(k, self.beta)))
            if ll <= p < rr:
                return k

        return bound - 1

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        prob = self.__get_alpha(len(vector)) / len(vector)

        # todo: move _distribution to tool funcs
        distribution = self._distribution(prob, len(vector))
        for i, value in enumerate(distribution):
            if prob > value:
                vector[i] = not vector[i]

        return individual.make_copy(vector)

    def __info__(self):
        return {
            **super().__info__(),
            'beta': self.beta
        }


__all__ = [
    'Doer'
]
