from ..mutation import Mutation

from typings.searchable import Searchable


class OneBit(Mutation):
    slug = 'mutation:one-bit'

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        i = self.random_state.randint(0, len(vector))

        vector[i] = not vector[i]
        return individual.make_copy(vector)


__all__ = [
    'OneBit'
]
