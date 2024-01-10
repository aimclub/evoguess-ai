from ..mutation import Mutation

from typings.optional import Int
from typings.searchable import Searchable


class FixSize(Mutation):
    slug = 'mutation:fix_size'

    def __init__(self, size: int, random_seed: Int = None):
        self.size = size
        super().__init__(random_seed)

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        i = self.random_state.randint(0, len(vector))
        vector[i] = not vector[i]

        if sum(vector) > self.size:
            indexes = [
                i for i, bit in enumerate(vector) if bit
            ]
            j = self.random_state.randint(0, len(indexes))
            vector[indexes[j]] = not vector[indexes[j]]

        return individual.make_copy(vector)


__all__ = [
    'FixSize'
]
