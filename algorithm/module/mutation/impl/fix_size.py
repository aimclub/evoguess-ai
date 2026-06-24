from ..mutation import Mutation

from typings.optional import Int
from typings.searchable import Searchable


class FixSize(Mutation):
    slug = 'mutation:fix_size'

    def __init__(self, size: int, flip_scale: float = 1.,
                 random_seed: Int = None):
        self.size = size
        self.flip_scale = flip_scale
        super().__init__(random_seed)

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        prob = self.flip_scale / len(vector)

        distribution = self._distribution(prob, len(vector))
        for i, value in enumerate(distribution):
            if prob > value:
                vector[i] = not vector[i]

        count = int(sum(vector)) - self.size
        if count != 0:
            indexes = [
                i for i, bit in enumerate(vector)
                if (count < 0) ^ int(bit)
            ]
            selected = self.random_state.choice(
                indexes, abs(count), replace=False
            )
            for index in selected:
                vector[index] = not vector[index]

        return individual.make_copy(vector)


__all__ = [
    'FixSize'
]
