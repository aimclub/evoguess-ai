from ..mutation import Mutation

from typings.optional import Int
from typings.searchable import Searchable


class Uniform(Mutation):
    slug = 'mutation:uniform'

    def __init__(self, flip_scale: float = 1., random_seed: Int = None):
        self.flip_scale = flip_scale
        super().__init__(random_seed)

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        prob = self.flip_scale / len(vector)

        # todo: move _distribution to tool funcs
        distribution = self._distribution(prob, len(vector))
        for i, value in enumerate(distribution):
            if prob > value:
                vector[i] = not vector[i]

        return individual.make_copy(vector)

    def __info__(self):
        return {
            **super().__info__(),
            'flip_scale': self.flip_scale
        }


__all__ = [
    'Uniform'
]
